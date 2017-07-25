# encoding=utf-8


import json
import logging

from models.user import UserModel
from handler.base import BaseHandler



class UserBindHandler(BaseHandler):

	def initialize(self):
		super(UserBindHandler, self).initialize()


	def get(self):
		self.render('login.html')


	def post(self):
		number = self.get_argument('number')
		uname = self.get_argument('uname')
		mobile = self.get_argument('mobile')
		email = self.get_argument('email')

		usermodel = UserModel()
		usermodel.number = str(number)
		usermodel.uname = uname
		usermodel.mobile = mobile
		usermodel.email = email
		usermodel.wx_id = self.userid
		try:
			status, resp = self.wcep.get_user(self.access_token, self.userid)
			logging.info(json.dumps(resp))
			usermodel.wx_avatar = resp['avatar']
		except Exception ,e:
			logging.error('Error to get user info from wx: %s' % str(e))
		
		ret = dict(errCode = 0, errMsg = '')
		try:
			usermodel.save()
		except Exception, e:
			logging.error('Error to bind user :%s' % str(e))
			ret['errCode'] = 1
			ret['errMsg'] = 'User bind failed'

		self.write(json.dumps(ret))
		self.finish()
