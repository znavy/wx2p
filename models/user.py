#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

import time
import peewee
from datetime import datetime


from .base import BaseModel



class UserModel(BaseModel):

	id = peewee.PrimaryKeyField()
	number = peewee.CharField(max_length = 10)
	uname = peewee.CharField(max_length = 50)
	password = peewee.CharField(max_length = 50)
	email = peewee.CharField(max_length = 64)
	mobile = peewee.CharField(max_length = 11)
	wx_id = peewee.CharField(max_length = 50)
	wx_avatar = peewee.CharField(max_length = 200)
	active = peewee.IntegerField(default = 1)


	class Meta:
		db_table = 't_user'
