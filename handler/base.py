#!usr/bin/env python
#-*- coding:utf-8 -*-

import time
import redis
import logging
import tornado.web
from datetime import datetime

from lib.sendmail import SendMail


class BaseHandler(tornado.web.RequestHandler):
	
	def initialize(self):
		super(BaseHandler, self).initialize()
		
		self._redis = self.settings.get('_redis')
		self.wcep = self.settings.get('wcep')
		at_key = self.settings.get('access_token')
		access_token = self._redis.get(at_key)
		if access_token:
			self.access_token = access_token
		else:
			self.access_token = self.wcep.get_access_token()
			if self.access_token and self._redis:
				self._redis.set(at_key, self.access_token, ex = 7200)
				
				
	def prepare(self):
		self.add_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-eval'; "
                        "connect-src 'self'; img-src 'self' data:; style-src 'self'; "
                        "font-src 'self'; frame-src 'self'; ")
		self.add_header("X-Frame-Options", "deny")
		self.add_header("X-XSS-Protection", "1; mode=block")
		self.add_header("X-Content-Type-Options", "nosniff")
		self.add_header("x-ua-compatible:", "IE=edge,chrome=1")
		self.clear_header("Server")


	def _set_event_count(self):
		cur_date_str = datetime.now().strftime('%Y-%m-%d')
		if self._redis:
			count = self._redis.get(cur_date_str)
			if count:
				self._redis.set(cur_date_str, int(count)+1)
			else:
				self._redis.set(cur_date_str, 1)
