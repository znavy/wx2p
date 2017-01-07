#!/opt/anaconda2/bin/python2.7
#coding=utf-8


import peewee


class DB(object):
	
	def __init__(self, kw):
		self.db_config = kw
		self.db = peewee.MySQLDatabase(self.db_config.pop('db'), **self.db_config)


	def connect(self):
		self.db.connect()


	def close(self):
		try:
			self.db.close()
		except:
			pass
