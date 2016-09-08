#encoding=utf-8

from fabric.api import cd ,run, env, hosts, execute, settings


class Deploy(object):
    def __init__(self):
	pass
    
    
    def app_deploy(self, key, script):
        hosts = {
            'ct25': {'ip':'10.0.0.25', 'user': 'appman', 'password': 'Appman@ct666', 'home_dir': '/opt/apache-tomcat-6.0.45'},
            'ct26': {'ip':'10.0.0.26', 'user': 'appman', 'password': 'Appman@ct666', 'home_dir': '/opt/apache-tomcat-6.0.45'},
            'report': {'ip':'10.0.0.29', 'user': 'appman', 'password': 'appman', 'home_dir': '/opt/report'},
            'wxapp': {'ip':'192.168.1.234', 'user': 'appman', 'password': 'appman', 'home_dir': '/opt/tomcat/wxpp'},
            'ows': {'ip':'10.0.0.38', 'user': 'appman', 'password': 'appman', 'home_dir': '/opt/apache-tomcat-7.0.70'}
        }
        
        host = hosts[key]

        env.host_string = host['ip']
        env.user = host['user']
        env.password = host['password']
        
        path = host['home_dir']

        with settings(warn_only = True): 
            with cd(path):
                run("./%s.sh" % script, pty = False)
