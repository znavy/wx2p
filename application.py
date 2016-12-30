#!/opt/anaconda2/bin/python2.7

import os
import sys
import time
import yaml
import redis
import logging
import logging.config

import tornado.web
import tornado.ioloop
from redis.exceptions import ConnectionError
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.options import options, define, parse_command_line

import handler
#from schedulers.health_check import _check
#from schedulers.bad_guy import find_bad_guy
from lib.wechat_sdk import WeChatEnterprise
from lib.util import get_config_from_yaml, get_redis


root_path = os.path.dirname(__file__)

define("config", default=os.path.join(
    root_path, "config.yaml"), help="config file's full path")
define("port", default="8888", help="Application port")
parse_command_line()

settings = {
    "static_path": os.path.join(root_path, "static"),
    "template_path": os.path.join(root_path, "templates")
}

# log config
logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

# global config
config = {}
try:
    config = get_config_from_yaml(options.config)
except yaml.scanner.ScannerError, e:
    print 'Error Document Format: %s' % e
    sys.exit(0)
except IOError:
    print '[Errno 2] No such file or directory: %s' % options.config
    sys.exit(0)
# MySQL

# Redis
_redis = None
try:
    redis_host = config['redis'].get('host', '127.0.0.1')
    redis_port = config['redis'].get('port', 6379)
    redis_db = config['redis'].get('db', 1)

    _redis = get_redis(redis_host, redis_port, redis_db)
    # test connection
    # Check is Redis server  available ?
    timestamp = str(int(time.time()))
    _redis.set('isAvailable', timestamp, ex=1)
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
    wcep = WeChatEnterprise(params)
    settings['wcep'] = wcep
except:
    print 'WeChat util init failed, some paramters missing maybe...'

# mail
settings['mail'] = config.get('mail')

# Schedulers
'''
try:
    scheduler = TornadoScheduler()
    scheduler.add_job(_check, trigger = 'interval', args = [settings.get('wcep')], seconds = 60)
    scheduler.start()
except Exception, e:
    print 'Schedulers start failed: %s' % str(e)
'''
urls = [
    (r'/', 'handler.index.IndexHandler'),
    (r'/login', 'handler.index.LoginHandler'),
    (r'/smsSwitch', 'handler.deploy.SmsSwitchHandler'),
    (r'/deploy', 'handler.deploy.IndexHandler'),
    (r'/sendText', 'handler.wechat.SendTextHandler'),
    (r'/getDpmt', 'handler.wechat.DepartmentHandler'),
    (r'/user', 'handler.wechat.UserHandler'),
    (r'/sendTextAsync', 'handler.test.TestHandler'),
]

app = tornado.web.Application(urls, **settings)

try:
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
except (KeyboardInterrupt, SystemExit):
    sys.exit(0)
except:
    import traceback
    print traceback.print_exc()
finally:
    sys.exit(0)
