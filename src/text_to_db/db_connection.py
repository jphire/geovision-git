# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "sundo"
__date__ = "$May 24, 2011 3:33:22 PM$"

import os
import psycopg2

def initiate_connection(database_name=os.getlogin(), username=os.getlogin(), password=None):
	if username is 'tkt_gvis':
		passwordfile = open(os.environ['HOME'] + '/.psql_password')
		password = passwordfile.readline().strip()
	connection_information = ("dbname=" + database_name
							  + "user=" + username
							  + "password=" + password)

	db_connection = psycopg2.connect(connection_information)
	return db_connection