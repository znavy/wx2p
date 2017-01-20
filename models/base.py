#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

import json

from bootloader import load_db
#from playhouse.signals import Model as _model
from peewee import Model

class BaseModel(Model):
	
	def __init__(self):
		super(BaseModel, self).__init__()


	def __str__(self):
		r = {}
		for k in self._data.keys():
			try:
				r[k] = getattr(self, k)
			except:
				r[k] = json.dumps(getattr(self, k))
		return json.dumps(r)


	class Meta:
		database = load_db()
