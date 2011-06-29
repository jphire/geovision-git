import os
import string

from geovision.viz.models import DbEntry
import re


class DbfileParser:
	def __init__(self, source_file, source=None):
		self.filename = source_file
		self.textfile = open(self.filename, 'r')
		self.source = source or self.filename[self.filename.rfind('/')+1:].split('.')[0]
		self.nextline = self.textfile.readline()
		self.dnadata = ''
		self.infoline = []
		self.id = ''
		self.description = ''
		# Uniprot-specific fields
		self.sub_db = ''
		self.entry_name = ''
		self.os_field = ''
		self.other_info = ''
		#
		self.dbname = ''
		if self.source.find("uniprot") != -1:
			self.dbname = "uniprot"
		elif self.source.find("frnadb") != -1:
			self.dbname = "frnadb"

	def next_db_entry(self):
		"""
		Function for reading database fasta file entries one at a time.
		Parsing is slightly different for different databases.
		Uniprot: OS= field is parsed separately, id field is split into components
		Frnadb: lcl| prefix in ID fields is removed
		"""
		if len(self.nextline) is 0:
			return None
		self.dnadata = ''
		self.infoline = self.nextline.strip().strip('>').split(None, 1)
		self.id = self.infoline[0]
		if self.dbname is "uniprot":
			split_id = self.id.split("|")
			self.id = split_id[1]
			self.sub_db = split_id[0]
			self.entry_name = split_id[2]
			self.infoline = self.infoline[1].split('OS=')
			self.description = self.infoline[0].strip()
			next_pattern_start = re.search(re.compile('[A-Z]{2}='), self.infoline[1]).start()
			self.os_field = self.infoline[1][:next_pattern_start-1]
			self.other_info = self.infoline[1][next_pattern_start:]
		elif self.dbname is "frnadb":
			self.description = self.infoline[1]
			self.id = self.id.split('|')[1]
			self.sub_db = ''
			self.entry_name = ''
			self.os_field = ''
			self.other_info = ''
		else:
			self.description = self.infoline[1]
			self.sub_db = ''
			self.entry_name = ''
			self.os_field = ''
			self.other_info = ''
		self.nextline = self.textfile.readline()
		while (self.nextline[0] is not '>'):
			self.dnadata += self.nextline.strip()
			self.dnadata = string.translate(self.dnadata, None, string.whitespace)
			self.nextline = self.textfile.readline()
			if len(self.nextline) is 0:
				break

		return DbEntry(source_file = self.source, db_id = self.id,
				description = self.description, sub_db = self.sub_db, entry_name = self.entry_name,
				os_field = self.os_field, other_info = self.other_info, data = self.dnadata)
