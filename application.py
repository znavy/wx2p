#!/usr/local/bin/python2.7

import os
import yaml
import logging
import logging.config

import tornado.ioloop
import tornado.web
from tornado.log import access_log, gen_log, app_log, LogFormatter

import handler


# log config

logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

settings = {
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "template_path":os.path.join(os.path.dirname(__file__), "templates")
}

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

