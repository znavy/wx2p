#!/opt/anaconda2/bin/python2.7

import logging
from celery import Celery
from lib.util import get_config_from_yaml


conf_path = '../config'


broker = 'redis://172.17.99.53:6379/0'
backend = 'redis://172.17.99.53:6379/1'

def make_celery():
	celery = Celery("tasks", broker = broker, backend = backend)
	celery.conf.update(
		CELERY_TIMEZONE = 'Asia/Shanghai',
		CELERY_RESULT_SERIALIZER='json',
		CELERY_TASK_RESULT_EXPIRES = 18000,
	)

	return celery

celery = make_celery()
