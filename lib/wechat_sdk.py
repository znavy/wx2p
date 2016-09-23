# -*- coding:utf-8 -*-

import json
import logging
import requests as r


class ErrorCode(object):
    SUCCESS = 0

class WeChatEnterprise(object):
    def __init__(self, params):
        self.redis = params.get('redis')
        self.agentid = params.get('agentID')
        self.corpid = params.get('CorpID')
        self.corpsecret = params.get('Secret')
        self.url_prefix = params.get('URL_PREFIX')
        #self.access_token = self.get_access_token()


    def get_access_token(self):
        if self.redis is not None:
            access_token = self.redis.get('access_token')
            if access_token:
                return access_token

        url = "%s/gettoken?corpid=%s&corpsecret=%s" % (self.url_prefix, self.corpid, self.corpsecret)
        try:
            resp = r.get(url)
            access_token = resp.json().get("access_token")
        except:
            access_token = None

        try:
            if self.redis is not None:
                self.redis.set('access_token', access_token, ex = 7200)
        except:
            pass
        
        return access_token


    @staticmethod
    def __response(resp):
        errcode = resp.get("errcode")
        if errcode is ErrorCode.SUCCESS:
            return True, resp
        return False, resp


    def __post(self, url, data):
        resp = r.post(url, data=json.dumps(data).decode('unicode-escape').encode("utf-8")).json()
        return self.__response(resp)


    def __get(self, url):
        resp = r.get(url).json()
        return self.__response(resp)


    def send_msg2user(self, access_token, content, to_user = None, to_ptmt = None, to_tag = None, safe = 0 ,msg_type = "text", **kwargs):
        url = "%s/message/send?access_token=%s" % (self.url_prefix, access_token)
        data = {
            "safe": safe, 
            "msgtype": msg_type, 
            "agentid": self.agentid
        }
        logging.info('Method send_msg2user > access_token: %s' % access_token)       
        messages = {"text": dict(content = content), 
                    "image": dict(media_id = kwargs.get("media_id")), 
                    "voice": dict(media_id = kwargs.get("media_id")),
                    "video": dict(media_id = kwargs.get("media_id"), title = kwargs.get("title"), 
                            description = kwargs.get("descritption")),
                    "file": dict(media_id = kwargs.get("media_id")),
                    "news": kwargs, 
                    "mpnews": kwargs,
        }
        data[msg_type] = messages[msg_type]

        if to_user is None:
            touser = "@all"
        else:
            touser = '|'.join(to_user)
        data["touser"] = touser
        
        if to_ptmt is not None:
            data["toparty"] = to_ptmt

        if to_tag is not None:
            data["totag"] = to_tag
        print data
        status, resp = self.__post(url, data)
        return status, resp


    def get_department_list(self, access_token):
        url = "%s/department/list?access_token=%s" % (self.url_prefix, access_token)
        status, resp = self.__get(url)
        return status, resp


    def create_user(self, access_token, data):
        url = "%s/user/create?access_token=%s" % (self.url_prefix, access_token)
        if data.get("userid") and data.get("name"):
            status, resp = self.__post(url, data)
        else:
            status, resp = False, 'userid or name is empty'
        return status, resp


    def second_validation(self, userid):
        pass
