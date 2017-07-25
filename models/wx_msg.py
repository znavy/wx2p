#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

import time
import peewee
from datetime import datetime

from .base import BaseModel


class WxMsgSendDetailModel(BaseModel):

	id = peewee.PrimaryKeyField()
	clock = peewee.IntegerField(default = int(time.time()), index = True)
	content = peewee.CharField(max_length = 300)
	send_to = peewee.CharField(max_length = 50, index = True)
	uptime = peewee.IntegerField(default = int(time.time()))

	class Meta:
		db_table = 't_wx_msg_send_detail'



class WxMsgStats(BaseModel):
		
	id = peewee.PrimaryKeyField()
	clock = peewee.IntegerField(default = int(time.time()), index = True)
	content = peewee.CharField(max_length = 300)
	send_to = peewee.CharField(max_length = 50)
	process_status = peewee.IntegerField(default = 0)
	uptime = peewee.IntegerField(default = int(time.time()))
	eventid = peewee.IntegerField(default = 0)
	host_group = peewee.CharField(max_length = 50)
	host = peewee.CharField(max_length = 100)
	ip = peewee.CharField(max_length = 20)
	hostname = peewee.CharField(max_length = 100)
	hostid = peewee.IntegerField(default = 0)
	
	
	class Meta:
		db_table = 't_wx_msg_stats'
