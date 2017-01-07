#encoding=utf-8


import json
import time
import logging

from tornado import gen
from tornado.web import asynchronous

import handler.base
from ..models.wx_msg import WxMsgSendDetailModel


class EventHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(EventHandler, self).initialize()
		self.wxModel = WxMsgSendDetailModel()

	
	def get(self, event_id):
		msg = WxMsgSendDetailModel.get(event_id = event_id)
		self.render('event.html', msg = msg)


	def post(self, event_id):
		msg = WxMsgSendDetailModel.get(event_id = event_id)
		msg.uptime = int(time.time())
		msg.save()
