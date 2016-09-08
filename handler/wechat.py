#encoding=utf-8

import json

import handler.base
from lib.wechat_sdk import WeChatEnterprise


class SendTextHandler(handler.base.BaseHandler):
    def __init__(self, *args, **argkws):
        super(SendTextHandler, self).__init__(*args, **argkws)
        self.wcep = WeChatEnterprise(access_token = self.access_token, agentID = 2)


    def get(self):
        user_str = self.get_argument("to_user", None)
        users = user_str.split('|') if user_str is not None else None
        
        content = self.get_argument("content", "Hello World")
        
        status, resp = self.wcep.send_msg2user(content, to_user = users, to_ptmt = None)
        
        if not status:
            self.set_status(500)
        else:
            self.set_status(200)
        self.finish()



class DepartmentHandler(handler.base.BaseHandler):
    def __init__(self, *args, **argkws):
        super(DepartmentHandler, self).__init__(*args, **argkws)
        self.wcep = WeChatEnterprise(access_token = self.access_token, agentID = 2)


    def get(self):
        status, resp = self.wcep.get_department_list()
        self.write(json.dumps(dict(status = status, resp = resp)))
        self.finish()



class UserHandler(handler.base.BaseHandler):
    def __init__(self, *args, **argkws):
        super(UserHandler, self).__init__(*args, **argkws)
        self.wcep = WeChatEnterprise(access_token = self.access_token, agentID = 2)


    def get(self):
        pass


    def post(self):
        userid = self.get_argument("userid")
        name = self.get_argument("name")
        department = department = self.get_argument("department")
        mobile = self.get_argument("mobile")

        data = dict(userid = userid, name = name, mobile = mobile, department = department)
        status, resp = self.wcep.create_user(data)
        self.write(json.dumps(dict(status = status, resp = resp)))
        self.finish()

