#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

from application import db
from playhouse.signals import Model as _model


class BaseModel(_model):
	
	def __init__(self):
		self.db = db


	class Meta:
		database = db
