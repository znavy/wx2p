#!/opt/anaconda2/bin/python2.7
#encoding=utf-8


import os
import sys
import time
import redis
from pyzabbix import ZabbixAPI
from redis.exceptions import ConnectionError

from lib.database import DB
from lib.wechat_sdk import WeChatEnterprise
from lib.util import get_config_from_yaml, get_redis


root_path = os.path.dirname(__file__)
conf_path = os.path.join(root_path, "config.yaml")

# global config
config = get_config_from_yaml(conf_path)

# MySQL
def load_db():
	db = DB(config['mysql'])
	
	return db.db


# Redis
def load_redis():
	redis_host = config['redis'].get('host', '127.0.0.1')
	redis_port = config['redis'].get('port', 6379)
	redis_db = config['redis'].get('db', 0)
	
	pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db, max_connections = 100)
	return pool


# wechat
def load_wechat():
	params = config.get('wechat')
	wcep = WeChatEnterprise(params)
	
	return wcep	


def load_wxcnf():
	return config.get('wechat')

def load_redis_conf():
	return config.get('redis')


def zabbix():
	zabbix_url =  config['zabbix']['api_url']
	zabbix_header = {"Content-Type":"application/json"} 
	zabbix_user   = config['zabbix']['user']
	zabbix_pass   = config['zabbix']['passwd']
	auth_code     = ""

	zapi = ZabbixAPI(zabbix_url)
	zapi.session.auth = (zabbix_user, zabbix_pass)
	zapi.session.verify = False
	zapi.timeout = 15.1
	zapi.login(zabbix_user, zabbix_pass)

	return zapi


def a10_conf():
	return config.get('A10')


server_port = config['server'].get('port', 8888)
access_token = config['server'].get('access_token', 'access_token')

# Schedulers
'''
try:
	scheduler = TornadoScheduler()
	scheduler.add_job(_check, trigger = 'interval', args = [settings.get('wcep')], seconds = 60)
	scheduler.start()
except Exception, e:
	print 'Schedulers start failed: %s' % str(e)
'''
