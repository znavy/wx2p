#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

import time
import peewee
from datetime import datetime

from .base import BaseModel


class WxMsgSendDetailModel(BaseModel):

	def __init__(self):
		super(WxMsgSendDetailModel, self).__init__()


	id = peewee.PrimaryKeyField()
	clock = peewee.IntegerField(default = int(time.time()), index = True)
	content = peewee.CharField(max_length = 300)
	send_to = peewee.CharField(max_length = 50, index = True)
	process_status = peewee.IntegerField(default = 0, index = True)
	uptime = peewee.IntegerField(default = int(time.time()))
	issue_head_id = peewee.IntegerField(default = 0)
	issue_type_id = peewee.IntegerField(default = 0)

	class Meta:
		db_table = 't_wx_msg_send_detail'
