#!/opt/anaconda2/bin/python2.7
#encoding=utf-8


import peewee

from .base import BaseModel


class IssueHeadModel(BaseModel):
	
	def __init__(self):
		super(IssueHeadModel, self).__init__()


	id = peewee.PrimaryKeyField()
	name = peewee.CharField(max_length = 30)

	class Meta:
		db_table = 't_issue_head'



class IssueTypeModel(BaseModel):

	def __init__(self):
		super(IssueTypeModel, self).__init__()

	id = peewee.PrimaryKeyField()
	name = peewee.CharField(max_length = 30)

	class Meta:
		db_table = 't_issue_type'
