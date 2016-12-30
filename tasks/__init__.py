#!/opt/anaconda2/bin/python2.7

import os
import logging
from celery import Celery

from lib.util import get_config_from_yaml, get_redis


conf_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),'config.yaml'))

config = get_config_from_yaml(conf_path)


broker = 'redis://127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/1'

try:
	broker = config['celery']['broker']
	backend = config['celery']['backend']
except Exception, e:
	logging.error(str(e))

def make_celery():
    celery = Celery("tasks", broker = broker, backend = backend)
    celery.conf.update(
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TASK_RESULT_EXPIRES=18000,
    )

    return celery

celery = make_celery()
