# encoding=utf-8

import handler.base
from tasks import wechat


class TestHandler(handler.base.BaseHandler):

    def initialize(self):
        super(TestHandler, self).initialize()

    def get(self):
        content = self.get_argument('content', 'Hello World')
        to_user = self.get_argument('to_user', 'heruihong')

        resp = wechat.send_wx_msg.delay(content, to_user)
        self.write(str(resp))
