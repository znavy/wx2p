import os
import time
from . import celery
from datetime import datetime

from lib.wechat_sdk import WeChatEnterprise



@celery.task
def echo(msg, timestamp=False):
    time.sleep(3)
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg


@celery.task
def add(x, y):
    time.sleep(3)
    return x + y


@celery.task
def send_wx_msg(content, to_user, to_ptmt = None):
    status, resp = wechat.send_msg2user(content, to_user = users, to_ptmt = to_ptmt)
    return 'wtf'
