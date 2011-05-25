# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sundo"
__date__ ="$May 24, 2011 3:33:22 PM$"

import psycopg2
import os
import sample_parser

class DbInsert:
	def __init__(self, db_name = os.getlogin(), user_name = os.getlogin(), password = None):
		self.database_name = db_name
		self.username = user_name
		if self.username is 'tkt_gvis':
			passwordfile = open(os.environ['HOME'] + '/.psql_password')
			self.password = passwordfile.readline().strip()


	def initiate_db_connection(self):
		connection_information = ("dbname=" + self.database_name
			+ "user=" + self.username
			+ "password=" + self.password)
			
		db_connection = psycopg2.connect(connection_information)
		return db_connection

	def text_to_dbtable():
		db_connection = initiate_db_connection()
		db_cursor = db_connection.cursor()
		source_file = "test.txt" # TODO: take parameter
		text_parser = sample_parser.SamplefileParser(source_file)
		item_to_insert = text_parser.next_read()
		while item_to_insert is not None:
			db_cursor.execute("INSERT INTO viz_read (source_file, read_id, description, data) VALUES (%s, %s, %s, %s)",
				(source_file, item_to_insert.readid, item_to_insert.description, item_to_insert.data))