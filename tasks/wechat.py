import os
import time
from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from lib.wechat_sdk import WeChatEnterprise


broker = 'redis://10.0.0.28:6379/0'
#broker='amqp://h2r:h2r123123@192.168.1.118/h2r_vhost'
backend = 'redis://10.0.0.28:6379/1'
#backend = 'rpc://'


celery = Celery("tasks", broker = broker, backend = backend)
'''
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_RESULT_BACKEND = 'amqp',
    CELERY_TASK_RESULT_EXPIRES = 18000,
)
'''


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
    #status, resp = wcep.send_msg2user(content, to_user = users, to_ptmt = to_ptmt)
    return 'wtf'


CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(minute = '*/1'),
        'args': (16, 16),
    },
}
