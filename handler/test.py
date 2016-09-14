#encoding=utf-8

import tcelery
from tasks import tasks
from tornado import gen
from tornado.web import asynchronous

import handler.base


tcelery.setup_nonblocking_producer()

class TestHandler(handler.base.BaseHandler):
    def initialize(self):
        super(TestHandler, self).initialize()

    
    @asynchronous
    @gen.coroutine
    def get(self):
        #resp = tasks.echo.apply_async(args = ['Hello world!'], callback = self.on_result)
        #content = self.get_argument('content', 'Test')
        #tasks.send_wx_msg.apply_async(args = [content, ['heruihong']], callback = self.on_result)
        #resp = yield gen.Task(tasks.echo.apply_async, args=['WTF'])
        resp = tasks.echo.delay('XixixiHahaha')
        self.write(str(resp))
        self.finish()


    def on_result(self, response):
        self.write(str(response.result))
        self.finish()
