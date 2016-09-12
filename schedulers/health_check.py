#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

import json
import logging
import requests as r
from datetime import datetime


urls = {
    'chitu25':'http://10.0.0.25:8080/ZHWL/flex/TMSLogin.html',
    'chitu26':'http://10.0.0.26:8080/ZHWL/flex/TMSLogin.html',
    'ows':'http://10.0.0.38:8080/f'
}

users = ['heruihong']

def _check(wecp):
    for k, v in urls.items():
        try:
            r.get(v, timeout = 0.5)
            log = str(datetime.now()) + ' ' + str(k) +': normal'
            logging.info(log)
        except Exception, e:
            # send wx msg
            content = '%s request timeout' % k
            logging.info(content)
            wecp.send_msg2user(content, to_user = users, to_ptmt = None)
