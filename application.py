#!/usr/local/bin/python2.7

import os
import sys
import time
import yaml
import redis
import logging
import logging.config

import tornado.web
import tornado.ioloop
from tornado.options import options, define, parse_command_line
from tornado.log import access_log, gen_log, app_log, LogFormatter
from redis.exceptions import ConnectionError

from apscheduler.schedulers.tornado import TornadoScheduler

import handler
from schedulers.health_check import _check
from lib.wechat_sdk import WeChatEnterprise


define("config", default="./config.yaml", help="config file's full path")
parse_command_line()

settings = {
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "template_path":os.path.join(os.path.dirname(__file__), "templates")
}

# log config
logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

# global config
config = {}
try:
    with open(options.config) as f:
        config = yaml.load(f)
except:
    print 'Cound not found confin.yaml file'
    sys.exit(0)

# Redis
_redis = None
try:
    redis_host = config['redis'].get('host', '127.0.0.1')
    redis_port = config['redis'].get('port', 6379)
    redis_db = config['redis'].get('db', 1)

    pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db)
    _redis = redis.Redis(connection_pool=pool)
    # test connection
    # Check is Redis server  available ?
    timestamp = str(int(time.time()))
    _redis.set('isAvailable', timestamp, ex = 1)
except KeyError:
    print 'Can not connect Redis server, check your config.yaml'
    sys.exit(0)
except ConnectionError:
    print 'Error to connecting to %s:%s. Connection refused' % (redis_host, redis_port)
else:
    settings['_redis'] = _redis

# wechat
try:
    params = config.get('wechat')
    params['redis'] = settings.get('_redis')
    wcep = WeChatEnterprise(params)
    settings['wcep'] = wcep
except:
    print 'WeChat util init failed, some paramters missing maybe...'

# Schedulers
try:
    scheduler = TornadoScheduler()
    scheduler.add_job(_check, trigger = 'interval', args = [settings.get('wcep')], seconds = 60)
    scheduler.start()
except Exception, e:
    print 'Schedulers start failed: %s' % str(e)

urls = [
    (r'/', 'handler.index.IndexHandler'),
    (r'/login', 'handler.index.LoginHandler'),
    (r'/smsSwitch', 'handler.deploy.SmsSwitchHandler'),
    (r'/deploy', 'handler.deploy.IndexHandler'),
    (r'/sendText', 'handler.wechat.SendTextHandler'),
    (r'/getDpmt', 'handler.wechat.DepartmentHandler'),
    (r'/user', 'handler.wechat.UserHandler'),
    (r'/test', 'handler.test.TestHandler')
]

app = tornado.web.Application(urls, **settings)

try:
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
except (KeyboardInterrupt, SystemExit):
    pass
except:
    raise

