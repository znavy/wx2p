#!usr/bin/env python
#-*- coding:utf-8 -*-

import time
import json
import redis
import urllib
import logging
import tornado.web
import requests as r
from datetime import datetime

from lib.a10 import A10SDK
from lib.sendmail import SendMail



class BaseHandler(tornado.web.RequestHandler):
	
	def initialize(self):
		super(BaseHandler, self).initialize()
		
		pool = self.settings.get('pool')
		self._redis = redis.Redis(connection_pool = pool)
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
		#self.add_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-eval'; "
        #                "connect-src 'self'; img-src 'self' data:; style-src 'self'; "
        #                "font-src 'self'; frame-src 'self'; ")
		self.add_header("X-Frame-Options", "deny")
		self.add_header("X-XSS-Protection", "1; mode=block")
		self.add_header("X-Content-Type-Options", "nosniff")
		self.add_header("x-ua-compatible:", "IE=edge,chrome=1")
		self.clear_header("Server")
		if not self._is_pass_outh():
			self._outh()


	def _is_pass_outh(self):
		uri = self.request.uri
		white_list = ['/sendText', '/sendTextAsync', '/ws', '/wsapi', '/eventList', '/pushAlert']
		return uri in white_list

	
	def _outh(self):
		self.userid = self._get_current_user()
		if self.userid is None:
			code = self.get_argument('code', None)
			if code:
				logging.info('Got code %s' % code)
				uid = self.getUid(code)
				self.userid = uid
				self._set_current_user(uid)
			else:
				logging.info('Not code given....')
				self.getcode()


	def _set_event_count(self):
		cur_date_str = datetime.now().strftime('%Y-%m-%d')
		if self._redis:
			count = self._redis.get(cur_date_str)
			if count:
				self._redis.set(cur_date_str, int(count)+1)
			else:
				self._redis.set(cur_date_str, 1)


	def _get_current_user(self):
		return self.get_secure_cookie("userid")


	def _set_current_user(self, userid):
		self.set_secure_cookie("userid", userid, expires_days = 30)


	def getUid(self, code):
		base_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?'
		params = dict(access_token = self.access_token)
		params['code'] = code
		url = base_url + urllib.urlencode(params)
		resp = r.get(url)
		try:
			logging.info('Getuserinfo resp: %s' % resp.text)
			data = json.loads(resp.text)
			return data['UserId'] if data.has_key('UserId') else data.get('OpenId', None)
		except Exception, e:
			logging.error('getuserinfo error: %s' % str(e))
			return None


	def getcode(self):
		wxcnf = self.settings.get('wxcnf')
		params = dict(appid = wxcnf['CorpID'])
		params['redirect_uri'] = wxcnf['redirect_uri']
		params['response_type'] = 'code'
		params['scope'] = 'snsapi_base'
		params['state'] = 'STATE#wechat'
		urlstr = urllib.urlencode(params)
		url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' + urlstr
		logging.info('url:%s' % url)
		self.redirect(url)


	def str2ts(self, s, format):
		dt = datetime.strptime(s, format)
		return int(time.mktime(dt.timetuple()))


	def ts2str(self, ts):
		ts = int(ts)
		return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


	def get_a10_session_id(self, a10sdk):
		session_id = self._redis.get('a10_session_id')
		if session_id is None:
			logging.info('A10 session_id %s from server' % session_id)		
			session_id = a10sdk.get_session_id()
			self._redis.set('a10_session_id', session_id, ex = 180)
		else:
			logging.info('A10 session_id %s from redis' % session_id)

		return session_id


	def _get_tts_tok(self):
		ttsconf = self.settings['config']['tts']
		tok = self._redis.get('tts_tok')
		if tok is None:

			params = dict(grant_type = 'client_credentials', 
					client_id = ttsconf['apikey'],client_secret = ttsconf['secretkey'])
			bdtts = 'https://openapi.baidu.com/oauth/2.0/token'
			resp = r.get(bdtts, params = params)
			data = json.loads(resp.text)
			tok = data['access_token']
			expires_in = data['expires_in']
			self._redis.set('tts_tok', tok, ex = int(expires_in))
			
		return tok

