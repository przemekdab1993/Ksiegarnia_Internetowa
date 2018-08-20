import mysql.connector

""" Dane  logowania do bazy danych """

class DBco:
	def __init__(self, dbconfig : dict) -> None:
		self.config = dbconfig
	
	def __enter__(self) -> 'cursor':
		self.conn = mysql.connector.connect(**self.config)
		self.cursor = self.conn.cursor()
		return self.cursor
	def __exit__(self, exc_type, exc_value, exc_trace) -> None:
		self.conn.commit()
		self.cursor.close()
		self.conn.close()