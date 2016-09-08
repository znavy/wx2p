#!usr/bin/env python
#-*- coding:utf-8 -*-

import time
import redis
import logging
import tornado.web

#from lib import config
import setting
from lib.wechat_sdk import WeChatEnterprise


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self,*argc,**argkw):
        super(BaseHandler,self).__init__(*argc,**argkw)
        try:
            pool = redis.ConnectionPool(host = setting.R_HOST, port = setting.R_PORT, db = setting.R_DB)
            self._redis = redis.Redis(connection_pool=pool)
            
            timestamp = str(int(time.time()))
            # Check is Redis server  available ?
            self._redis.set('isAvailable', timestamp, ex = 1)
        except Exception, e:
            logging.error(str(e))
            self._redis = None

        wcep = WeChatEnterprise(access_token = None, agentID = 2)
        self.access_token = None

        if self._redis is not None:
            access_token = self._redis.get("access_token")
            if access_token:
                self.access_token = access_token
            else:
                access_token = wcep.get_access_token()
                if access_token is not None:
                    self.access_token = access_token
                    self._redis.set("access_token", access_token, ex = 7200)
