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
#from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.options import options, define, parse_command_line

import handler
from bootloader import load_redis, load_wechat, server_port, access_token, load_wxcnf, a10_conf


root_path = os.path.dirname(__file__)
#define("port", default="8888", help="Application port")
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
	settings['wxcnf'] = load_wxcnf()
except Exception, e:
	print 'Failed to init wechat: %s' % str(e)
	sys.exit(0)

settings['access_token'] = access_token
settings['a10_conf'] = a10_conf()

urls = [
    (r'/', 'handler.index.IndexHandler'),
    (r'/login', 'handler.user.UserBindHandler'),
    (r'/smsSwitch', 'handler.deploy.SmsSwitchHandler'),
    (r'/deploy', 'handler.deploy.IndexHandler'),
    (r'/sendText', 'handler.wechat.SendTextHandler'),
    (r'/getDpmt', 'handler.wechat.DepartmentHandler'),
    (r'/user', 'handler.wechat.UserHandler'),
    (r'/sendTextAsync', 'handler.wechat.SendTextAsyncHandler'),
	(r'/alertblock', 'handler.alert.BlockHandler'),
	(r'/restarthost', 'handler.alert.RestartHostsHandler'),
	(r'/trigger', 'handler.zabbix.ZabbixTriggerHandler'),
	(r'/tag', 'handler.wechat.TagHandler'),
	(r'/issue/(\d+?)', 'handler.issue.IssueHandler'),
	(r'/vports', 'handler.a10.VServerMemberHandler'),
	(r'/vsmembers', 'handler.a10.ServiceGroupHandler'),
	(r'/test', 'handler.wechat.TestHandler')
]

app = tornado.web.Application(urls, cookie_secret = '0b507c24-0fd9-4adf-87f0-d9d72b229d57' ,**settings)

try:
    app.listen(server_port)
    tornado.ioloop.IOLoop.instance().start()
except (KeyboardInterrupt, SystemExit):
    sys.exit(0)
except:
    import traceback
    print traceback.print_exc()
finally:
    sys.exit(0)
