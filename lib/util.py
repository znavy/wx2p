#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,random
from tornado.options import options,define
import json
import yaml
import time
import logging
import hashlib
import requests as r
from urllib import unquote
from xml.etree import ElementTree as ET

import redis
#from lib.redis import PRedis

define('token',default='itrying',help='developer id ,unique')
define('url', default = 'https://api.weixin.qq.com/cgi-bin/token', help = '')
define('grant_type',default = 'client_credential', help='')
define('appid',default='wxbcf3b4f02a34b29a',help='')
define('secret',default='341eb89888c06b03e207120ee20f57cc',help='')


def get_token():
    pass

def create_sign(nonce=None,timestamp=None):
    '''
        
    '''
    if nonce is None and timestamp is None:
        nonce=_getNonce()
        timestamp=_getTimestamp()
      
    signdict={'token':'pwcds','nonce':nonce,'timestamp':timestamp}
    tmp_list = sorted(signdict.items(), key=lambda x:x[1])
    signstr=''
    for t in tmp_list:
        signstr+=str(t[1])
    sign=hashlib.sha1(signstr).hexdigest()
    signdict['sign']=sign
 
    return signdict


def parseXml(msgStr):
    msgbody = None
    try:
    	root=ET.fromstring(msgStr)
    	msgbody = {}
    	for child in root:
            msgbody[child.tag]=child.text
    except Exception, e:
        pass
    return msgbody


def toXMLStr(msgBodyDict):
    xmlStr='<xml>'
    for key in msgBodyDict:
        xmlStr+='<%s><![CDATA[%s]]></%s>' % (key,msgBodyDict[key],key)
    xmlStr+='</xml>'
    return xmlStr


def buildMsgDict(content, openid, msg_type, user):
    if content in [None, '']:
        content = 'No response is available.'
    
    d = dict(Content = content)
    d['ToUserName'] = openid
    d['FromUserName'] = user
    d['CreateTime'] = str(int(time.time()))
    d['MsgType'] = msg_type
    
    return d


def _getTimestamp():
    return str(int(time.time()*1000))

def _getNonce():
    return random.randint(100000,1000000)


def get_redis(redis_host, redis_port, redis_db = 0):
    pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db)
    return redis.Redis(connection_pool=pool)


def get_config_from_yaml(file):
    with open(file) as f:
        return yaml.load(f)


if __name__ == '__main__':
    creatSign()
