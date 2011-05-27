#coding: UTF-8
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "lassetyr"
__date__ = "$23.5.2011 15:12:48$"

from geovision.viz.models import Read as ReadModel
# TODO: muuta käyttämään djangon ORBia

class SamplefileParser:
	def __init__(self, source_file):
		self.filename = source_file
		self.textfile = open(self.filename, 'r')
		self.nextline = self.textfile.readline()
		self.dnadata = ''
		self.infoline = []

	def next_read(self):
		if len(self.nextline) is 0:
			return None
		self.dnadata = ""
		self.infoline = self.nextline.strip().strip('>').split(None, 1)
		if len(self.infoline) < 2:
			self.infoline.append('')
		self.nextline = self.textfile.readline()
		while (self.nextline[0] is not '>'):
			self.dnadata += self.nextline.strip()
			self.nextline = self.textfile.readline()
			if len(self.nextline) is 0:
				break
		return ReadModel.objects.create(sample = self.filename, read_id = self.infoline[0], description = self.infoline[1], data = self.dnadata)

#
#class DbWriter:
#	def __init__(self, filename='test.txt'):
#		self.db_conn = db_connection.initiate_connection()
#		self.filename = filename
#
#
#	def read_samples_to_dbtable(self):
#		db_cursor = self.db_conn.cursor()
#		source_file = self.filename
#		try:
#			text_parser = SamplefileParser(source_file)
#		except IOError:
#			print 'Unable to open file ' + self.filename
#			raise
#		read_to_insert = text_parser.next_read()
#		while read_to_insert is not None:
#			db_cursor.execute("INSERT INTO viz_read (source_file, read_id, description, data) VALUES (%s, %s, %s, %s)",
#				(source_file, read_to_insert.readid, read_to_insert.description, read_to_insert.data))
