import os
import time
import json
import logging
import requests as r
from celery.schedules import crontab
from datetime import datetime, timedelta

from . import celery, config
from lib.util import get_redis
from bootloader import load_wechat, zabbix

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

@celery.task(name = "alert_agg")
def alert_agg():
	redis = get_redis(config['redis']['host'], config['redis']['port'])
	try:
		now = int(time.time())
		before5min = now - (60 * 5)
		for k in ['alertjmx', 'alertagent']:
			count = redis.zcount(k, before5min, now)
			count = int(count)
			print '%s, %s' % (k, count)
			eventid = redis.zrangebyscore(k, before5min, now)
			if count > 0:
				#zbx = zabbix()
				#hosts = zbx.host.get(host = '' output = ['name'])
				#hosts = [host['name'] for host in hosts]
				#print 'hosts: %s' % ','.join(hosts)
				wechat = load_wechat()
				access_token = wechat.get_access_token()
				triggers = dict(alertjmx = 'Trigger JMX IS UNREACHABLE was triggered %s times in 5 minutes' % str(count), 
						alertagent='Trigger ZBX AGENT IS UNREACHABLE war triggered %s times in 5 minutes' % str(count))
				content = triggers[k]
				send_wx_msg.delay(access_token, content, ['heruihong'])
	except Exception, e:
		print str(e)


celery.conf.update(
	CELERYBEAT_SCHEDULE = {
		'perminute': {'task': 'alert_agg', 'schedule': crontab(minute='*/5')}
		}
)
