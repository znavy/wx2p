#!/opt/anaconda2/bin/python2.7
#encoding=utf-8

from bootloader import load_db
from playhouse.signals import Model as _model


class BaseModel(_model):
	
	def __init__(self):
		super(BaseModel, self).__init__()


	class Meta:
		database = load_db()
