# encoding=utf-8

import json
import logging

from tornado import gen
from tornado.web import asynchronous

import handler.base
from tasks import wechat
from models.wx_msg import WxMsgSendDetailModel


class SendTextHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(SendTextHandler, self).initialize()
		self.wxModel = WxMsgSendDetailModel()
		
	
	@asynchronous
	@gen.coroutine
	def get(self):
		args = self.request.arguments
		logging.info('arguments: %s' % json.dumps(args))
		
		user_str = self.get_argument("to_user", None)
		content = self.get_argument("content", None)
		if None in [user_str, content]:
			ret = dict(errCode=10001, errMsg='Missing parameter to_user/content')
			self.write(json.dumps(ret))
			self.finish()
			return
		
		try:
			self.wxModel.content = content
			self.wxModel.send_to = user_str
			self.wxModel.save()
			issue_id = self.wxModel.id
		except:
			logging.error('Message content saved failed:%a' % content)

		users = user_str.split(',') if not isinstance(user_str, list) else user_str
		
		if self._redis and self._redis.get('link'):
			link = "<a href='http://%s/issue/%s'>点我</a>" % (self.request.headers.get('Host'), issue_id)
			content = '%s %s' % (content, link)
		
		status, resp = self.wcep.send_msg2user(self.access_token, content, to_user=users, to_ptmt=None)
		if not status:
			logging.error('Response from wx: ' + json.dumps(resp))
			ret = dict(errCode = 10002, errMsg = resp)
		else:
			ret = dict(errCode = 0, errMsg='')
		
		# Set event count
		try:
			self._set_event_count()
		except:
			pass

		self.write(json.dumps(ret))
		self.finish()
		
		
	def post(self):
		self.get()
		
		

class SendTextAsyncHandler(handler.base.BaseHandler):

	def initialize(self):
		super(SendTextAsyncHandler, self).initialize()

	
	def get(self):
		content = self.get_argument('content', None)
		user_str = self.get_argument('to_user', None)
		if None in [content, user_str]:
			self.write(json.dumps(dict(errCode = 10001, errMsg = 'Missing parameter to_user/content')))
			return

		users = user_str.split(',')
		resp = wechat.send_wx_msg.delay(self.access_token, content, users)

		# Set event count
		try:
			self._set_event_count()
		except:
			pass
	
		ret = dict(errCode = 0, errMsg = str(resp))
		self.write(json.dumps(ret))


	def post(self):
		self.get()


		
class DepartmentHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(DepartmentHandler, self).initialize()
		
		
	def get(self):
		status, resp = self.wcep.get_department_list(self.access_token)
		self.write(json.dumps(dict(status=status, resp=resp)))
		
		

class UserHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(UserHandler, self).initialize()
		
		
	def get(self):
		pass
	
	
	def post(self):
		userid = self.get_argument("userid")
		name = self.get_argument("name")
		department = department = self.get_argument("department")
		mobile = self.get_argument("mobile")
		
		data = dict(userid=userid, name=name, mobile=mobile, department=department)
		
		status, resp = self.wcep.create_user(self.access_token, data)
				
		self.write(json.dumps(dict(status=status, resp=resp)))
		self.finish()
