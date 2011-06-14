# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sundo"
__date__ ="$Jun 14, 2011 6:06:37 PM$"

import os
import string
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'

from geovision.viz.models import DbEntry as DbEntryModel
import re

FIELD_PATTERN = re.compile('[A-Z]{2}=')

class DbfileParser:
	def __init__(self, source_file, source=None):
		self.filename = source_file
		self.textfile = open(self.filename, 'r')
		self.source = source or self.filename[self.filename.rfind('/')+1:]
		self.nextline = self.textfile.readline()
		self.dnadata = ''
		self.infoline = []
		self.id = ''
		self.description = ''
		self.os_field = ''
		self.other_info = ''
		self.uniprot = self.source.find("uniprot")

	def next_read(self):
		if len(self.nextline) is 0:
			return None
		self.dnadata = ''
		self.infoline = self.nextline.strip().strip('>').split(None, 1)
		self.id = self.infoline[0]
		self.infoline = self.infoline[1].split('OS=')
		self.description = self.infoline[0]
		next_pattern_start = re.search(FIELD_PATTERN, self.infoline[1]).start()
		self.os_field = self.infoline[1][:next_pattern_start-1]
		self.other_info = self.infoline[1][next_pattern_start:]
		self.nextline = self.textfile.readline()
		while (self.nextline[0] is not '>'):
			self.dnadata += self.nextline.strip()
#       For the files that have whitespace in the data, uncomment the next line:
			self.dnadata = string.translate(self.dnadata, None, string.whitespace)
			self.nextline = self.textfile.readline()
			if len(self.nextline) is 0:
				break

		return DbEntryModel(source_file = self.source, db_id = self.id,
				description = self.description, os_field = self.os_field,
				other_info = self.other_info, data = self.dnadata)