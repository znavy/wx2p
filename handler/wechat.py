# encoding=utf-8

import json
import logging

from tornado import gen
from tornado.web import asynchronous

import handler.base


class SendTextHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(SendTextHandler, self).initialize()
		
	
	@asynchronous
	@gen.coroutine
	def get(self):
		args = self.request.arguments
		logging.info('arguments: %s' % json.dumps(args))
		
		user_str = self.get_argument("to_user", None)
		content = self.get_argument("content", None)
		event_id = self.get_argument("event_id", 0)
		if None in [user_str, content, event_id]:
			ret = dict(errCode=10001, errMsg='Missing parameter to_user/content/event_id')
			self.write(json.dumps(ret))
			self.finish()
			return
		
		users = user_str.split('|') if not isinstance(user_str, list) else user_str
		#link = '<a href="http://alert.ane56.com/event/%s">Hit Me</a>' % event_id
		#content = '%s %s' % (content, link)
		logging.info(content)
		status, resp = self.wcep.send_msg2user(self.access_token, content, to_user=users, to_ptmt=None)
		if not status:
			logging.error('Response from wx: ' + json.dumps(resp))
		else:
			self.set_status(200)
		self.finish()
		
		
	def post(self):
		self.get()
		
		
		
class DepartmentHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(DepartmentHandler, self).initialize()
		
		
	def get(self):
		status, resp = self.wcep.get_department_list(self.access_token)
		self.write(json.dumps(dict(status=status, resp=resp)))
		self.finish()
		
		

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
