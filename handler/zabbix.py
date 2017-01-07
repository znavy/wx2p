


import time
import json
import pandas as pd
from datetime import datetime
from pyzabbix import ZabbixAPI

import handler.base


zabbix_url="http://monitor.mspcloud.cn/api_jsonrpc.php" 
zabbix_header = {"Content-Type":"application/json"} 
zabbix_user   = "anneng" 
zabbix_pass   = "ane@56" 
auth_code     = ""


class ZabbixTriggerHandler(handler.base.BaseHandler):

	def initialize(self):
		super(ZabbixTriggerHandler, self).initialize()
		
		self.zapi = ZabbixAPI(zabbix_url)
		self.zapi.login(zabbix_user, zabbix_pass)


	def get(self):
		self.render('trigger.html')


	def post(self):
		unack_triggers = self.zapi.trigger.get(only_true=1, skipDependent=1, monitored=1, 
				active=1, expandDescription=1, expandData='host', 
				withLastEventUnacknowledged=1, min_severity = 4, 
				output = ["triggerid","description","priority"])
		triggers  = pd.DataFrame(unack_triggers)
		xx = triggers.groupby('host').count()['hostid']
		yy = xx.copy()
		yy.sort_values(inplace = True)
		
		self.write(yy.to_json())
