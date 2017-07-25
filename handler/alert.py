# encoding=utf-8

import json
import time
import logging
from datetime import datetime

from tasks import wechat
from models.wx_msg import WxMsgStats
from handler.base import BaseHandler


class BlockHandler(BaseHandler):

	def initialize(self):
		super(BlockHandler, self).initialize()


	def get(self):
		zbx_groups = self._redis.get('zbx_groups')
		if zbx_groups is None:
			zbx_groups = list()
		else:
			zbx_groups = json.loads(zbx_groups)

		self.render('alert_block.html', groups = zbx_groups)


	def post(self):
		print json.dumps(self.request.arguments)
		groupids = self.get_argument('groupids', None)
		time_from = self.get_argument('time_from', None)
		time_till = self.get_argument('time_till', None)
		reason = self.get_argument('reason', None)

		if None in [groupids, time_from, time_till, reason]:
			res = dict(errCode = 1, errMsg = 'Missing parameter(s)')
			self.write(json.dumps(res))
			return

		time_from = self.str2ts(time_from, '%Y/%m/%d %H:%M')
		time_till = self.str2ts(time_till, '%Y/%m/%d %H:%M')
		if time_from >= time_till:
			res = dict(errCode = 2, errMsg = 'Invalid parameter(s)')
			self.write(json.dumps(res))
			return

		alertModel = AlertBlockModel()
		alertModel.groupids = groupids
		alertModel.creator = self.userid
		alertModel.hostids = ''
		alertModel.time_from = time_from
		alertModel.time_till = time_till
		alertModel.reason = reason
			
		try:
			alertModel.save()
			_id = alertModel.id
			wechat.send_wx_msg.delay(self.access_token, 'application id:%s' % _id, ['heruihong'])
		except Exception, e:
			res = dict(errCode = 3, errMsg = 'Application failed!')
			self.write(json.dumps(res))
			logging.error('Application failed: %s' % str(e))

		res = dict(errCode = 0, errMsg = 'Done')
		self.write(json.dumps(res))



class RestartHostsHandler(BaseHandler):

	def initialize(self):
		super(RestartHostsHandler, self).initialize()


	def get(self):
		day = self.get_argument('day', None)
		
		hosts = self._get_rhosts(day)

		self.render('restarthosts.html', hosts = hosts)


	def post(self):
		day = self.get_argument('day', None)

		hosts = self._get_rhosts(day)

		self.write(json.dumps(hosts))


	def _get_rhosts(self, day):
		if day is None:
			day = datetime.today().strftime('%Y/%m/%d')

		ts_start = int(time.mktime(time.strptime(day +' 00:00:00', '%Y/%m/%d %H:%M:%S')))
		ts_end = int(time.mktime(time.strptime(day + ' 23:59:59', '%Y/%m/%d %H:%M:%S')))

		msgs = WxMsgStats.select().where((WxMsgStats.clock >= ts_start) & (WxMsgStats.clock <= ts_end) & (WxMsgStats.content % '%restart%'))
		
		res = list()
		for msg in msgs:
			d = dict(clock = self.ts2str(msg.clock), ip = msg.ip)
			res.append(d)
		print res	
		return res
