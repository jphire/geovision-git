#coding: UTF-8
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "lassetyr"
__date__ = "$23.5.2011 15:12:48$"

import os
import string
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'

from geovision.viz.models import Read as ReadModel, DbEntry as DbEntryModel

class SamplefileParser:
	def __init__(self, source_file, sample=None, is_db=False):
		self.filename = source_file
		self.textfile = open(self.filename, 'r')
		self.sample = sample or self.filename[self.filename.rfind('/')+1:]
		self.nextline = self.textfile.readline()
		self.dnadata = ''
		self.infoline = []
		self.is_db = is_db

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
#       For the files that have whitespace in the data, uncomment the next line:
			self.dnadata = string.translate(self.dnadata, None, string.whitespace)
			self.nextline = self.textfile.readline()
			if len(self.nextline) is 0:
				break
		if self.is_db:
			return DbEntryModel(source_file = self.sample, read_id = self.infoline[0], description = self.infoline[1], data = self.dnadata)
		else:
			return ReadModel(sample = self.sample, read_id = self.infoline[0], description = self.infoline[1], data = self.dnadata)
