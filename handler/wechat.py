# encoding=utf-8

import re
import json
import time
import logging

from tornado import gen
from tornado.web import asynchronous

import handler.base
from tasks import wechat
from models.wx_msg import WxMsgSendDetailModel, WxMsgStats


class SendTextHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(SendTextHandler, self).initialize()
		self.wxModel = WxMsgSendDetailModel()
		self.p_jmx = re.compile("(.+?) JMX is not reachable")
		self.p_agent = re.compile("Zabbix agent on (.+?) is unreachable for 5 minutes")

	
	@asynchronous
	@gen.coroutine
	def get(self):
		args = self.request.arguments
		logging.info('arguments: %s' % json.dumps(args))
		
		user_str = self.get_argument("to_user", None)
		content = self.get_argument("content", None)

		is_match = self.p_jmx.search(content) or self.p_agent.search(content)
		if is_match:
			self.write(json.dumps(dict(errCode = 0, errMsg='pass')))
			self.finish()
			return

		if None in [user_str, content]:
			ret = dict(errCode=10001, errMsg='Missing parameter to_user/content')
			self.write(json.dumps(ret))
			self.finish()
			return
		
		try:
			self.wxModel.content = content
			self.wxModel.send_to = user_str
			self.wxModel.clock = int(time.time())
			self.wxModel.uptime = int(time.time())
			self.wxModel.save()
			issue_id = self.wxModel.id
		except Exception, e:
			logging.error('Message content saved failed:%s' % str(e))

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
		

		self.write(json.dumps(ret))
		self.finish()
		
		
	def post(self):
		self.get()
		
		

class SendTextAsyncHandler(handler.base.BaseHandler):

	def initialize(self):
		super(SendTextAsyncHandler, self).initialize()
		self.p_jmx = re.compile("(.+?) JMX is not reachable")
		self.p_agent = re.compile("Zabbix agent on (.+?) is unreachable for 5 minutes")

		
	def get(self):
		args = self.request.arguments
		logging.info('arguments: %s' % json.dumps(args))
		
		content = self.get_argument('content', None)
		content = json.loads(content)
		
		trigger_name = content['trigger_name']
		host = content['host']
		hostname = content['hostname']
		ip = content['ip']
		hostgroup = content['hostgroup']
		event_id = content['eventid']

		is_match = self.p_jmx.search(trigger_name) or self.p_agent.search(trigger_name)
		if is_match:
			self._agg(content)
			self.write(json.dumps(dict(errCode = 0, errMsg = 'pass')))
			self.finish()
			return

		user_str = self.get_argument('to_user', None)
		if None in [content, user_str]:
			self.write(json.dumps(dict(errCode = 10001, errMsg = 'Missing parameter to_user/content')))
			self.finish()
			return

		users = user_str.split(',')
		#resp = wechat.send_wx_msg.delay(self.access_token, trigger_name, users)
		resp = dict(errCode = 0, errMsg = '')

		issue_id = 0
		try:
			model = WxMsgStats()
			model.content = trigger_name
			model.send_to = user_str
			model.clock = int(time.time())
			model.uptime = int(time.time())
			model.eventid = event_id
			model.host_group = hostgroup
			model.host = host
			model.hostname = hostname
			model.ip = ip
			model.hostid = 0
			
			model.save()
			issue_id = model.id
		except Exception, e:
			logging.error('Message content saved failed:%s' % str(e))
	
		if self._redis and self._redis.get('link') and issue_id != 0:
			link = "<a href='http://%s/issue/%s'>点我</a>" % (self.request.headers.get('Host'), issue_id)

		ret = dict(errCode = 0, errMsg = str(resp))
		self.write(json.dumps(ret))


	def post(self):
		self.get()
	

	def _agg(self, content):
		trigger_name = content['trigger_name']
		eventid = int(content['eventid'])
		key = 'alertjmx' if self.p_jmx.search(trigger_name) else 'alertagent'
		ct = int(time.time())
		print type(ct), type(eventid),key
		self._redis.zadd(key, eventid, ct)



		
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

	
class TestHandler(handler.base.BaseHandler):

	def initialize(self):
		super(TestHandler, self).initialize()


	def get(self):
		wechat.alert_agg.delay()
