#!/opt/anaconda2/bin/python2.7
#-*- coding:utf-8 -*-

from __future__ import print_function
import json
import logging
import tornadoredis
import tornado.gen
from tornado import websocket

from .base import BaseHandler


class IndexHandler(BaseHandler):

	def initialize(self):
		super(IndexHandler, self).initialize()


	def get(self):
		self.render("eventList.html")



class SocketHandler(websocket.WebSocketHandler):

	def __init__(self, *args, **kwargs):
		super(SocketHandler, self).__init__(*args, **kwargs)
		redis_conf = self.settings['redis_conf']
		self._redis = tornadoredis.Client(host = redis_conf['host'], port = redis_conf['port'], selected_db = redis_conf['db'])
		self._redis.connect()
		self.listen()


	@tornado.gen.engine
	def listen(self):
		yield tornado.gen.Task(self._redis.subscribe, 'alert_channel')
		self._redis.listen(self.on_message)


	def on_message(self, msg):
		if msg.kind == 'message':
			self.write_message(msg.body)

		if msg.kind == 'disconnect':
			self.close()


	def on_close(self):
		if self._redis.subscribed:
			self._redis.unsubscribe('alert_channel')
			self._redis.disconnect()



class ApiHandler(BaseHandler):

	def initialize(self):
		super(ApiHandler, self).initialize()
		

	def get(self):
		self.finish()

		host = self.get_argument("host")
		content = self.get_argument("content")
		dt = self.get_argument("dt")
		eventid = self.get_argument("eventid")
		status = self.get_argument("status")

		tok = self._get_tts_tok()
		data = dict(host = host, content = content, dt = dt, eventid = eventid, status = status, tok= tok, is_sound = 1)
		logging.info(json.dumps(data))

		ret = self._redis.publish('alert_channel', json.dumps(data))


	def post(self):
		self.get()


class PushHistoryHandler(BaseHandler):

	def initialize(self):
		super(PushHistoryHandler, self).initialize()

	
	def get(self):
		alerts = self._redis.hgetall('alerts')
		alerts = [json.loads(a) for a in alerts.values()]

		ret = []
		for a in alerts:
			if int(a['status']) == 0:
				tmp = a
				tmp['is_sound'] = 0
				ret.append(tmp)

		self.write(json.dumps(ret))


	def post(self):
		eventid = self.get_argument('eventid', None)
		ret = dict(errCode = 0, errMsg = 'Done')
		if eventid is None:
			ret = dict(errCode = 1, errMsg = 'No eventid given')
		else:
			try:
				self._redis.hdel("alerts", eventid)
			except Exception, e:
				ret = dict(errCode = 2, errMsg = str(e))

		self.write(json.dumps(ret))
