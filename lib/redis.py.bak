import sys, os, time, redis, traceback, json
import logging

class PRedis():
    ''' Establish redis session connection pool '''
    def __init__(self, host, port, db = 0):
	self.host = host
	self.port = port
	self.db = db

	try:
	    pool=redis.ConnectionPool(host = self.host, port = self.port, db = self.db)
	    self.conn=redis.Redis(connection_pool = pool)
	    self.pipe=self.conn.pipeline()
	except:
	    #return traceback.format_exc()
	    return None

    def r_set(self, keys, values, ex):
	'''set'''
	try:
	    self.pipe.set(keys, json.dumps(values))
	    return self.pipe.execute()
	except:
	    return traceback.format_exc()


    def r_hset(self, key, field, values):
	'''hash > key,field,values'''
	try:
	    self.pipe.hset(key, field, json.dumps(values))
	    self.pipe.execute()
	except:
	    return traceback.format_exc()


    def r_hget(self, key, field = None):
	'''querying by key,return dict'''
	try:
	    fields=[]
	    if field:
		fields.append(field)
	    else:
		fields=self.conn.hkeys(key)
	    for f in fields:
		self.pipe.hget(key, f)
	    values=self.pipe.execute()
	    #print 'values:',values
	    values=[v for v in values]
	    return dict(zip(fields, values))
	except:
	    return traceback.format_exc()


    def r_get(self, argv):
	'''get single key'''
	try:
	    self.pipe.get(argv)
	    return json.loads(self.pipe.execute()[0])
	except:
	    return traceback.format_exc()


    def r_getkeys(self):
	'''get all keys'''
	try:
	    self.pipe.keys('*')
	    return self.pipe.execute()[0]
	except:
	    return False


    def r_del(self, keys):
	'''delete by keys'''
	try:
	    self.pipe.delete(keys)
	    return self.pipe.execute()
	except:
	    return False
