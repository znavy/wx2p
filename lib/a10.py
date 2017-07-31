

import socket, ssl
import httplib, json, urllib, urllib2


def connect_patched(self):
	"Connect to a host on a given (SSL) port."
	sock = socket.create_connection((self.host, self.port),self.timeout, self.source_address)
	if self._tunnel_host:
		self.sock = sock
		self._tunnel()
	
	self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


class A10SDK:

	def __init__(self, a10_server, username, password):
		self.a10_server = a10_server
		self.username = username
		self.password = password


	def get_session_id(self):
		httplib.HTTPSConnection.connect = connect_patched
		c = httplib.HTTPSConnection(self.a10_server)
		c.request("GET", "/services/rest/V2/?method=authenticate&username={0}&password={1}&format=json".format(self.username, self.password))
		response = c.getresponse()
		data = json.loads(response.read())
		session_id = data['session_id']

		return session_id


	def get_vport_by_vip(self, session_id, vip):
		url = "https://{0}/services/rest/V2/?&session_id={1}&format=json&method=slb.virtual_server.search".format(self.a10_server, session_id)
		parmas = dict(address= vip)
		req = urllib2.Request(url, json.dumps(parmas))
		rsp = urllib2.urlopen(req)
		res = json.loads(rsp.read())
		ports = list()
		vports = res['virtual_server']['vport_list']

		return vports


	def get_members_by_vname(self, session_id, name):
		url = "https://{0}/services/rest/V2/?&session_id={1}&format=json&method=slb.service_group.search".format(self.a10_server, session_id)
		parmas = dict(name= name)
		req = urllib2.Request(url, json.dumps(parmas))
		rsp = urllib2.urlopen(req)
		res = json.loads(rsp.read())
		
		members = res['service_group']['member_list']
		return members

	def connect_patched(self):
		"Connect to a host on a given (SSL) port."
		sock = socket.create_connection((self.host, self.port),self.timeout, self.source_address)
		if self._tunnel_host:
			self.sock = sock
			self._tunnel()

		self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
