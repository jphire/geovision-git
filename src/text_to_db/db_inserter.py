# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sundo"
__date__ ="$May 24, 2011 3:33:22 PM$"

import psycopg2

class DbInserter:
	def initiate_db_connection(self):
		database_name = "tkt_gvis"
		username = "tkt_gvis"
		passwordfile = open(os.environ['HOME'] + '/.psql_password')
		password = passwordfile.readline().strip()

		connection_information = ("dbname=" + database_name
			+ "user=" + username
			+ "password=" + password)

		db_connection = psycopg2.connect(connection_information)
		return db_connection

	def text_to_dbtable():
		db_connection = initiate_db_connection()
		db_cursor = db_connection.cursor()
		table_columns = data_to_insert.column_names()

		return None