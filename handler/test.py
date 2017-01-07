# encoding=utf-8

import json
import logging

import handler.base
from tasks import wechat
from models.wx_msg import WxMsgSendDetailModel


class TestHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(TestHandler, self).initialize()
	
	
	def get(self):
		content = self.get_argument('content', None)
		user_str = self.get_argument('to_user', None)
		if None in [content, user_str]:
			self.write(json.dumps(dict(errCode = 10001, errMsg = 'Missing parameter to_user/content')))
			return

		users = user_str.split('|')
		resp = wechat.send_wx_msg.delay(self.access_token, content, users)
		self.write(str(resp))



class ModelTestHandler(handler.base.BaseHandler):

	def initialize(self):
		super(ModelTestHandler, self).initialize()
		self.wxModel = WxMsgSendDetailModel()

	def get(self):
		content = self.get_argument('content', 'xxx')
		send_to = 'heruihong'
		event_id = 110
		self.wxModel.content = content
		self.wxModel.send_to = send_to
		self.wxModel.event_id = event_id

		self.wxModel.save()
