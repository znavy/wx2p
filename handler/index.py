#encoding=utf-8

import json
import logging
import tornado

import handler.base
import lib.util
from tornado.options import define, options
from fabric.api import execute

from lib.deploy import Deploy
from lib.wxBizMsgCrypt import WXBizMsgCrypt


define('Token', default = 'lprJ8GFg9mojuSk', help = '')
define('EncodingAESKey', default = 'RI3mMWIJnxgiSzTLV3VdVghArmqAyHtgSHK1sLxiwAC', help = '')
define('CorpID', default = 'wx74c026e563a3b7ed', help = '')


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
        #mysign = lib.util.create_sign(nonce = nonce, timestamp = timestamp)
	
        self.write(_echostr)
        self.finish() 
        '''
        self.redirect('/login')        

 
    def post(self):
	body = self.request.body
	body_str = body#.decode('utf-8')
        sign = self.get_argument('msg_signature')
        nonce = self.get_argument('nonce')
        timestamp = self.get_argument('timestamp')
        
        ret, xml_content = self.wxcpt.DecryptMsg(body_str, sign, timestamp, nonce)
        # logging.info('xml content: %s' % xml_content) 

        if ret in [0, '0']:
            rec_msg = lib.util.parseXml(xml_content)
            logging.info(json.dumps(rec_msg))
            if rec_msg is not None and rec_msg.get('MsgType', None) == 'text':
                users = [rec_msg.get('FromUserName', 'who')]
                result = self.cmdProcess(rec_msg)
                content = 'Command execution failed'
                if result:
                    content = 'Command execution successful'
                status, resp = self.wcep.send_msg2user(self.access_token, content, to_user = users, to_ptmt = None)
        else:
            logging.error('Decrypt message failed')
        
        self.write('success')
	self.finish()


    def cmdProcess(self, req):
        users = [req.get('FromUserName', 'who')]
        content = req.get('Content', '')
        creation = req.get('1470725839', 0)
        msg_id = req.get('MsgId', 0)
    
        hosts = ['ct25', 'ct26', 'report','ows']
        cmd_list = ['stop', 'startup', 'unpackage', 'replace_conf']
        tmplist = content.split('|')
        if len(tmplist) == 2 and tmplist[1] in cmd_list and tmplist[0] in hosts:
            hostname = tmplist[0]
            script = tmplist[1]
            logging.info('host: %s, script: %s' % (hostname, script))
            try:
                execute(self.deploy.app_deploy, hostname, script)
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
        args = {k : self.get_argument(k) for k in self.request.arguments}
        if args.has_key('username') and args.has_key('password') and self.check_auth(args):
            #ret = {'errCode':0, 'errMsg':'Done'}
            self._redis.set('session', 'haha', 30*60)
            #self.redirect('/deploy')
            ret = {'errCode':0, 'errMsg':'Done'}
        else:
            ret = {'errCode':1, 'errMsg':'Auth failed.'}

        self.write(json.dumps(ret))
        self.finish()


    def check_auth(self, args):
        return args['username']=='chunghwa56' and args['password']=='110'
