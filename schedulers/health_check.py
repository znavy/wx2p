#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

import yaml
import json
import socket
import logging
import requests as r
from datetime import datetime


config = {}
with open('schedulers/_config.yaml') as f:
    config = yaml.load(f)

http_urls = config.get('http', {})
tcp_list = config.get('tcp', {})
users = config.get('users', None)


def _check(wecp):
    _http(wecp)
    _tcp(wecp)


def _http(wecp):
    for k, v in http_urls.items():
        try:
            r.get(v, timeout=0.5)
            log = str(datetime.now()) + ' ' + str(k) + ': normal'
            logging.info(log)
        except Exception, e:
            # send wx msg
            content = '%s request timeout' % k
            logging.info(content)
            wecp.send_msg2user(content, to_user=users, to_ptmt=None)


def _tcp(wecp):
    for k, v in tcp_list.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((v['host'], v['port']))
            log = str(datetime.now()) + ': %s is alive' % k
        except Exception, e:
            log = str(datetime.now()) + ': Zabbix is down'
            wecp.send_msg2user(log, to_user=users, to_ptmt=None)

        logging.info(log)
