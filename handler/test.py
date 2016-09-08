#encoding=utf-8

import tcelery
from tasks import tasks
from tornado.web import asynchronous

import handler.base


tcelery.setup_nonblocking_producer()

class TestHandler(handler.base.BaseHandler):
    def __init__(self, *args, **argkws):
        super(TestHandler, self).__init__(*args, **argkws)

    
    @asynchronous
    def get(self):
        tasks.echo.apply_async(args = ['Hello world!'], callback = self.on_result)
        #tasks.add.apply_async(args = [1, 2])
        self.write('WTF')
        self.finish()
        #content = self.get_argument('content', 'Test')
        #tasks.send_wx_msg.apply_async(args = [content, ['heruihong']], callback = self.on_result)


    def on_result(self, response):
        self.write(str(response.result))
        self.finish()
