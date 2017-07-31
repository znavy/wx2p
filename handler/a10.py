# encoding=utf-8


import json
import logging
from IPy import IP

from lib.a10 import A10SDK
from .base import BaseHandler



class ServiceGroupHandler(BaseHandler):
	
	def initialize(self):
		super(ServiceGroupHandler, self).initialize()
		self.a10_conf = self.settings['a10_conf']	

	
	def post(self):
		print self.request.arguments
		service_group = self.get_argument('service_group', '')
		a10sdk = A10SDK(self.a10_conf['host'], self.a10_conf['username'], self.a10_conf['password'])
		session_id = self.get_a10_session_id(a10sdk)
		mem_list = a10sdk.get_members_by_vname(session_id, service_group)
		
		up= list()
		down = list()
		for m in mem_list:
			if m['status'] in [1, '1']:
				up.append('{0}:{1}'.format(m['server'], m['port']))
			else:
				down.append('{0}:{1}'.format(m['server'], m['port']))
		
		ret = dict(up = up, down = down)
		print ret
		self.write(json.dumps(ret))



class VServerMemberHandler(BaseHandler):

	def initialize(self):
		super(VServerMemberHandler, self).initialize()
		self.a10_conf = self.settings['a10_conf']

	def get(self):
		self.render('vs2member.html')


	def post(self):
		a10_addr = self.get_argument('a10_addr','')
		
		ret = None
		try:
			ip = IP('172.17.97.0/24')
			if a10_addr not in ip:
				ret = dict(errCode = 2, errMsg = 'Invalid ip address')
		except Exception, e:
			ret = dict(errCode=1, errMsg = str(e))
		
		if ret is not None:
			self.write(json.dumps(ret))
			self.finish()
			return
		
		a10sdk = A10SDK(self.a10_conf['host'], self.a10_conf['username'], self.a10_conf['password'])
		session_id = self.get_a10_session_id(a10sdk)
		vports = a10sdk.get_vport_by_vip(session_id, a10_addr)
		
		ret = dict(errCode = 0, errMsg = vports)
		self.write(ret)



class MemberVServerHandler(BaseHandler):

	def initialize(self):
		super(MemberVServerHandler, self).initialize()


	def get(self):
		pass


	def post(self):
		pass
