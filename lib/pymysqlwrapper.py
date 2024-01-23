#!/bin/env python3
"""\
pymysqlwrapper.py - This is a lightweight wrapper for Pymysql

"""
__project__	= "Lotteries Results Scrapper"
__part__	= 'Lightweight wrapper for Pymysql'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"
__status__	= "dev"

import pymysql

class pyMySQL():
	debug = 0
	sql = ''
	erno = 0
	error = ''
	connection = False
	cursor = False
	rowcount = 0
	autocommit  =True

	def __init__(self, host, user='', password='', db='', port=3306, debug=0, asdict=True):
		if type(host) is dict:
			self.host     = host['host']
			self.user     = host['user']
			self.password = host['password']
			self.db       = host['db']
		else:
			self.host     = host
			self.user     = user
			self.password = password
			self.db       = db
		self.port   = int(port)
		self.debug  = int(debug)
		self.asdict = pymysql.cursors.DictCursor if asdict else None
		try:
			self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, autocommit=self.autocommit )
		except Exception as e:
			if e.args:
				self.erno  = e.args[0]
				self.error = e.args[1]
			print('Connect to MySQL Server Failed, host=%s, user=%s, db=%s, port=%u, errmsg=%s' % (self.host, self.user, self.db, self.port, e))
			return None

	def __del__(self):
		self.disconnect()

	def disconnect(self):
		try:
			if self.connection:
				self.connection.close()
				self.sql = ''
				self.connection = False
				self.cursor = False
		except Exception as e:
			print('Disconnect to MySQL Server Failed, errmsg=%s' % (e))

	def query(self, sql):
		try:
			self.sql = sql
			self.cursor = self.connection.cursor(self.asdict)
			self.cursor.execute(sql)
			self.rowcount = self.cursor.rowcount
			if not self.asdict:
				self.fieldnames = [field[0] for field in self.cursor.description]
			output = self.cursor.fetchall()
			self.cursor.close()
			return output
		except Exception as e:
			if e.args:
				self.erno = e.args[0]
				self.error = e.args[1]
			if self.debug: print('Query failed: %s\n%s' % (sql, e))
			return None

	# insert returns lastrowid, indeed it is same "query"
	def insert(self, sql):
		try:
			self.query(sql)
			lastID = self.cursor.lastrowid
			self.rowcount = self.cursor.rowcount
			self.cursor.close()
			return lastID
		except Exception as e:
			if self.debug: print('Insert failed: %s\n%s' % (sql, e))
			return None

	# select reow one by one
	def queryone(self, sql):
		try:
			self.sql = sql
			self.cursor = self.connection.cursor(self.asdict)
			self.cursor.execute(sql)
			self.rowcount = self.cursor.rowcount
			return self.rowcount
		except Exception as e:
			if e.args:
				self.erno = e.args[0]
				self.error = e.args[1]
			if self.debug: print('Query failed: %s\n%s' % (sql, e))
			return None

	# get next selected row
	def nextrow(self):
		try:
			output = self.cursor.fetchone()
			if not output:
				self.cursor.close()
			return output
		except Exception as e:
			if e.args:
				self.erno = e.args[0]
				self.error = e.args[1]
			if self.debug: print('Nextrow failed: %s' % (e))
			return None


if __name__ == '__main__':
	print(f'{__project__}. {__part__}')

#	conf = {
#		'host': 'localhost',
#		'user': 'mserg',
#		'password': 'pass',
#		'db': 'database',
#	}
#	DB = pyMySQL(conf);

#	# get all rows at once
#	rows = DB.query('show tables')
#	if 0 == DB.erno:
#		for r in rows:
#			print(r)

#	# get rows one by one
#	rowcount = DB.queryone('show tables')
#	print(rowcount)
#	while rowcount:
#		res=DB.nextrow()
#		if not res: break
#		print(res)

