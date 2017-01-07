#!/opt/anaconda2/bin/python2.7

import os
import sys
import time
import yaml
import logging
import logging.config

import tornado.web
import tornado.ioloop
from redis.exceptions import ConnectionError
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.options import options, define, parse_command_line

import handler
from bootloader import load_redis, load_wechat


root_path = os.path.dirname(__file__)
define("port", default="8888", help="Application port")
parse_command_line()

# log config
logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

settings = {
    "static_path": os.path.join(root_path, "static"),
    "template_path": os.path.join(root_path, "templates"),
	"debug": False,
}

try:
	settings['_redis'] = load_redis()
except Exception, e:
	print 'Failed to init redis: %s' % str(e)
	sys.exit(0)

try:
	settings['wcep'] = load_wechat()
except Exception, e:
	print 'Failed to init wechat: %s' % str(e)
	sys.exit(0)

urls = [
    (r'/', 'handler.index.IndexHandler'),
    (r'/login', 'handler.index.LoginHandler'),
    (r'/smsSwitch', 'handler.deploy.SmsSwitchHandler'),
    (r'/deploy', 'handler.deploy.IndexHandler'),
    (r'/sendText', 'handler.wechat.SendTextHandler'),
    (r'/getDpmt', 'handler.wechat.DepartmentHandler'),
    (r'/user', 'handler.wechat.UserHandler'),
    (r'/sendTextAsync', 'handler.test.TestHandler'),
	(r'/xxoo', 'handler.test.ModelTestHandler'),
	(r'/trigger', 'handler.zabbix.ZabbixTriggerHandler'),
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
