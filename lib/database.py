#!/opt/anaconda2/bin/python2.7
#coding=utf-8


import peewee
from playhouse.signals import Model as _model


class DB(object):
	
	def __init__(self, kw):
		self.config = kw
		self.db = peewee.MySQLDatabase(self.config.pop('db'), **self.config)


	def connect(self):
		self.db.connect()


	def close(self):
		try:
			self.db.close()
		except:
			pass
