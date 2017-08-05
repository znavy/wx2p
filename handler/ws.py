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
		logging.info('-----msg body:{0}'.format(json.dumps(msg.body)))
		logging.info(msg.kind)
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
		
		if self._redis is None:
			logging.info('--------------ApiHandler redis is None---------')


	def get(self):
		self.finish()

		host = self.get_argument("host")
		content = self.get_argument("content")
		dt = self.get_argument("dt")
		eventid = self.get_argument("eventid")
		status = self.get_argument("status")

		data = dict(host = host, content = content, dt = dt, eventid = eventid, status = status)
		logging.info(json.dumps(data))

		ret = self._redis.publish('alert_channel', json.dumps(data))
		logging.info(str(ret))


	def post(self):
		self.get()
