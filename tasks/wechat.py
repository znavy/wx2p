import os
import time
import json
import logging
import requests as r
from datetime import datetime

from . import celery, config


agentid = config['wechat']['agentID']
corpid = config['wechat']['CorpID']
corpsecret = config['wechat']['Secret']
url_prefix = config['wechat']['URL_PREFIX']

def __response(resp):
	errcode = resp.get("errcode")
	if errcode == 0:
		return True, resp
	return False, resp
		
	
def __post(url, data):
	resp = r.post(url, data = json.dumps(data).decode('unicode-escape').encode("utf-8")).json()
	return __response(resp)
					
	
def __get(url):
	resp = r.get(url).json()
	return __response(resp)


@celery.task
def echo(msg, timestamp=False):
    time.sleep(3)
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg


@celery.task
def send_wx_msg(access_token, content, to_user = None, to_ptmt = None, to_tag = None, safe = 0, msg_type = "text", **kwargs):
	url = "%s/message/send?access_token=%s" % (url_prefix, access_token)
	data = {"safe": safe, "msgtype": msg_type, "agentid": agentid}
	logging.info('Method send_msg2user > access_token: %s' % access_token)
	messages = {"text": dict(content=content),
			"image": dict(media_id=kwargs.get("media_id")),
			"voice": dict(media_id=kwargs.get("media_id")),
			"video": dict(media_id=kwargs.get("media_id"), title=kwargs.get("title"),description=kwargs.get("descritption")),
			"file": dict(media_id=kwargs.get("media_id")),
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
	status, resp = __post(url, data)
	logging.info('Post data: %s' % json.dumps(data))
	return status, resp
