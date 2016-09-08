#!/usr/local/bin/python2.7


from fabric.api import cd, run, env, hosts

hosts = {
    'ct25': {'ip':'10.0.0.25', 'user': 'appman', 'password': 'Appman@ct666', 'home_dir': '/opt/apache-tomcat-6.0.45'},
    'ct26': {'ip':'10.0.0.26', 'user': 'appman', 'password': 'Appman@ct666', 'home_dir': '/opt/apache-tomcat-6.0.45'},
    'report': {'ip':'10.0.0.29', 'user': 'appman', 'password': 'appman', 'home_dir': '/opt/report'}
}

def remote_exec(key, script):
    host = hosts.get(key)
    if host is None:
        return

    env.hosts = [host['ip']]
    env.user = host['user']
    env.password = host['password']
    
    path = host['home_dir']

    with cd(path):
        run('./%s.sh' % script)

