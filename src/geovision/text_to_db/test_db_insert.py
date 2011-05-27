import unittest
import db_insert

class TestDbInsert(unittest.TestCase):
	def test_db_insert_connection(self):
		try:
			self.db_connection = db_insert.DbInsert.initiate_db_connection()
		except psycopg2.OperationalError:
			self.fail("Could not create db connection")

if __name__ == '__main__':
	unittest.main()