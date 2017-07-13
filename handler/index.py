# encoding=utf-8

import json
import logging

import handler.base
import lib.util
from tornado.options import define, options
from fabric.api import execute

from lib.deploy import Deploy
from lib.wxBizMsgCrypt import WXBizMsgCrypt


define('Token', default='9RCG4czBSkJJ6l2', help='')
define('EncodingAESKey',default='DvuavRvHBQiVzZaamVMaKjJbHNP5oIJeQBOssDetOQU', help='')
define('CorpID', default='wx06222e02032c9b2f', help='')


class IndexHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(IndexHandler, self).initialize()
		self.wxcpt = WXBizMsgCrypt(options.Token, options.EncodingAESKey, options.CorpID)
		self.deploy = Deploy()
		
		
	def get(self):
		'''
		sign = self.get_argument('msg_signature')
		nonce = self.get_argument('nonce')
		timestamp = self.get_argument('timestamp')
		echostr = self.get_argument('echostr')
		
		ret, _echostr = self.wxcpt.VerifyURL(sign, timestamp, nonce, echostr)
		
		self.write(_echostr)
		self.finish()
		'''
		self.redirect('/login')
		
		
	def post(self):
		body = self.request.body
		body_str = body  # .decode('utf-8')
		sign = self.get_argument('msg_signature')
		nonce = self.get_argument('nonce')
		timestamp = self.get_argument('timestamp')
		
		ret, xml_content = self.wxcpt.DecryptMsg(body_str, sign, timestamp, nonce)
		# logging.info('xml content: %s' % xml_content)
		if ret in [0, '0']:
			rec_msg = lib.util.parseXml(xml_content)
			logging.info(json.dumps(rec_msg))
			if rec_msg['FromUserName'] in ['heruihong']:
				self.cmdProcess(rec_msg)
		else:
			logging.error('Decrypt message failed')
			self.write('success')
			
		self.finish()
		
		
	def cmdProcess(self, req):
		users = [req.get('FromUserName', 'who')]
		content = req.get('Content', '')
		creation = req.get('1470725839', 0)
		msg_id = req.get('MsgId', 0)
		hosts = ['zbxs', 'zbxp1', 'zbxp2']
		cmd_list = ['start', 'stop', 'restart']
		tmplist = content.split('|')
		if len(tmplist) == 2 and tmplist[1] in cmd_list and tmplist[0] in hosts:
			hostname = tmplist[0]
			script = tmplist[1]
			try:
				ret = execute(self.deploy._exec, hostname, script)
				logging.info('Result of executing script: %s on host: %s is %s' % (script, hostname, str(ret)))
			except Exception, e:
				logging.error(str(e))
				return False
			return True
		else:
			logging.error('Invalid hosts or cmd_list')
			return False
		
		
	def msgHandle(self, xmlStr):
		msgDict = lib.util.parseXml(xmlStr)
		retMsg = None
		if msgDict and msgDict.has_key('MsgType') and msgDict['MsgType'] == 'text':
			if msgDict.has_key('Content') and msgDict['Content'] == 'chunghwa56':
				text = 'http://wx.chunghwa56.com/login'
			else:
				text = None
				to_msg_dict = lib.util.buildMsgDict(text, msgDict['FromUserName'], 'text', msgDict['ToUserName'])
				
				retMsg = lib.util.toXMLStr(to_msg_dict)
				
		return retMsg
	
	
class LoginHandler(handler.base.BaseHandler):
	
	def initialize(self):
		super(LoginHandler, self).initialize()
		
		
	def get(self):
		self.render('login.html')
		
		
	def post(self):
		args = {k: self.get_argument(k) for k in self.request.arguments}
		if args.has_key('username') and args.has_key('password') and self.check_auth(args):
			#ret = {'errCode':0, 'errMsg':'Done'}
			self._redis.set('session', 'haha', 30*60)
			# self.redirect('/deploy')
			ret = {'errCode': 0, 'errMsg': 'Done'}
		else:
			ret = {'errCode': 1, 'errMsg': 'Auth failed.'}
			
		self.write(json.dumps(ret))
		self.finish()
		
		
	def check_auth(self, args):
		return args['username'] == 'chunghwa56' and args['password'] == '110'
