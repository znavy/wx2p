#!/opt/anaconda2/bin/python2.7

from fabric.api import env, run, settings, execute



class Deploy:
	def __init__(self):
		self.hosts = {'zbxs':{'ip':'172.17.99.24','cmd':'service zabbix_server %s'}, 
					  'zbxp1':{'ip':'172.17.99.31','cmd':'service zabbix_proxy %s'},
					  'zbxp2':{'ip':'172.17.99.24','cmd':'service zabbix_proxy %s'}
				}


	def _exec(self, key, cmd):
		host = self.hosts[key]

		env.host_string = host['ip']
		env.user = 'zabbix'
		env.password = 'zabbix'

		with settings(warn_only = True):
			run(host['cmd'] % cmd)

