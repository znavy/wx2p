# encoding=utf-8


import json
import time
import logging
import datetime


#from playhouse.shortcuts import model_to_dict

import handler.base
from models.issue import IssueTypeModel
from models.wx_msg import WxMsgSendDetailModel


class IssueHandler(handler.base.BaseHandler):

	def initialize(self):
		super(IssueHandler, self).initialize()
		self.wxModel = WxMsgSendDetailModel
		self.isModel = IssueTypeModel

	def get(self, issue_id):
		ft = self.wxModel.id == issue_id
		try:
			issue = self.wxModel.get(ft)

			clock = int(issue.clock)
			clock = datetime.datetime.fromtimestamp(clock).strftime('%Y-%m-%d %H:%M:%S')
			issue.clock = clock

			types = self.isModel.select()
		except:
			issue = None
			raise
		
		self.render('issue.html', issue = issue, types = types)


	def post(self, issue_id):
		type_id = self.get_argument('type_id')
		
		ft = self.wxModel.id == issue_id
		issue = self.wxModel.get(ft)
		issue.issue_type_id = type_id
		issue.uptime = int(time.time())

		try:
			issue.save()
			ret = dict(errCode = 0, errMsg = '')
		except Exception, e:
			ret = dict(errCode = 110, errMsg = str(e))

		self.write(json.dumps(ret))
