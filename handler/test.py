# encoding=utf-8

import json

import handler.base
from tasks import wechat


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
