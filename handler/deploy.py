#encoding=utf-8

import os
import json
import logging
import tornado
from fabric.api import cd ,run, env, hosts, execute, settings

import handler.base
from lib.deploy import Deploy


class SmsSwitchHandler(handler.base.BaseHandler):
    def initialize(self):
        super(SmsSwitchHandler, self).initialize()
        if self._redis is None or self._redis.get('session') is None:
            self.redirect('/login')
        self.ret = dict(errCode = 0, errMsg = None)
        self.key = 'turn'


    def get(self):
        if self._redis:
            turn = self._redis.get(self.key)
            if turn:
                self.ret['errMsg'] = 'on'
            else:
                self.ret['errMsg'] = 'off'

        self.write(json.dumps(self.ret))
        self.finish()


    def post(self):
        if self._redis:
            turn = self._redis.get(self.key)
            if turn:
                x = self._redis.delete(self.key)
                if not x:
                    self.ret['errCode'] = 1
                    self.ret['errMsg'] = 'Failed(off)'
            else:
                x = self._redis.set(self.key, 'xixi')
                if not x:
                    self.ret['errCode'] = 1
                    self.ret['errMsg'] = 'Failed(on)'

        self.write(json.dumps(self.ret))
        self.finish()


class IndexHandler(handler.base.BaseHandler):
    def initialize(self):
        super(IndexHandler, self).initialize()
        self.deploy = Deploy()


    def get(self):
        if self._redis is None or self._redis.get('session') is  None:
            self.redirect('/login')
        
        self.render('index.html')


    def post(self):
        args = {k : self.get_argument(k) for k in self.request.arguments}

        if not args.has_key('hostname') or not args.has_key('script'):
            ret = {'errCode': 1, 'errMsg': 'Missing parameter'}
        else:
            try:
                result = execute(self.deploy.app_deploy, args['hostname'], args['script'])
            except Exception, e:
                result = e
            ret = {'errCode': 0, 'errMsg': str(result)}

        self.write(json.dumps(ret))
        self.finish()

