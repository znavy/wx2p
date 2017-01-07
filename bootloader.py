#!/opt/anaconda2/bin/python2.7
#encoding=utf-8


import os
import sys
import time
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
	
	_redis = get_redis(redis_host, redis_port, redis_db)
	# test connection
	# Check is Redis server  available ?
	timestamp = str(int(time.time()))
	_redis.set('isAvailable', timestamp, ex = 1)
	
	return _redis

# wechat
def load_wechat():
	params = config.get('wechat')
	wcep = WeChatEnterprise(params)
	
	return wcep	

# Schedulers
'''
try:
	scheduler = TornadoScheduler()
	scheduler.add_job(_check, trigger = 'interval', args = [settings.get('wcep')], seconds = 60)
	scheduler.start()
except Exception, e:
	print 'Schedulers start failed: %s' % str(e)
'''
