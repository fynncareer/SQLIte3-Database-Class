import os 
import datetime 
import sqlite3

class DB(object):	 
	"""DB initializes and manipulates SQLite3 databases."""

	def __init__(self, database, statements = None):
		"""Initialize a new or connect to an existing database.

		Accept setup statements to be executed.
		"""
		self.database = database

		self.connect()
		
		if statements:
			self.execute(statements)

		self.close()			

	def connect(self):

		self.connection = sqlite3.connect(self.database)
		self.cursor = self.connection.cursor()
		self.connected = True
		self.statement = ''

	def close(self): 

		self.connection.commit()
		self.connection.close()
		self.connected = False

	def execute(self, statements):
		
		queries = []
		close = False
		if not self.connected:
			#open a previously closed connection
			self.connect()
			#mark the connection to be closed once complete
			close = True
		if type(statements) == str:
			#all statements must be in a list
			statements = [statements]
		if statements:
			for statement in statements:
				#print(statement)
				try:
					#statement = self.statement.strip()
					#reset the test statement
					self.statement = ''
					#print(statement)
					self.cursor.execute(statement)
					#retrieve selected data
					data = self.cursor.fetchall()
					row = [row for row in data]
					#print(row)
					#print(data)
					if statement.upper().startswith('SELECT'):
						#append query results
						queries.append(row)
				except sqlite3.Error as error:
					print('An error occurred:', error.args[0])
					print('For the statement:', statement)
		if close: #only close the connection if opened in this function
			self.close()   
		
		return queries

		
		
if __name__ == "__main__":
	
	portfolio_db = DB('portfolio.db')
	
	portfolio_db.execute('''CREATE TABLE IF NOT EXISTS portfolio (username varchar(32), coin varchar(32), amount int, CONSTRAINT coin_constraint UNIQUE (coin));''')
	
	portfolio_db.execute('''INSERT INTO portfolio VALUES ("Bob", "Bitcoin", 10);''')
	
	results = portfolio_db.execute('''SELECT * FROM portfolio WHERE username = "Bob";''')
	print(results)
	
	portfolio_db.execute('''DELETE FROM portfolio WHERE username = "Bob";''')
		
 
	