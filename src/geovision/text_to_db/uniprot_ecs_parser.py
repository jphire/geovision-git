# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sundo"
__date__ ="$Jun 16, 2011 4:59:28 PM$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'

from geovision.viz.models import DbUniprotEcs as EcsEntry

class EcsFileParser:
	"""
	Parser for uniprot database ecs file.
	Creates one object per parsed line.
	"""
	def __init__(self, source_file):
		self.textfile = open(source_file, 'r')
		self.nextline = self.textfile.readline()
		self.db_id = ''
		self.pext = ''
		self.ecs = ''

	def next_ecs_entry(self):
		if len(self.nextline) is 0:
			return None
		while self.nextline[0] is '#': # Skip possible commentlines
			self.nextline = self.textfile.readline()
		split_line = self.nextline.strip().split("\t")
		self.db_id = split_line[0]
		self.pext = split_line[1]
		self.ecs = split_line[2]
		self.nextline = self.textfile.readline()
		
		return EcsEntry(db_id = self.db_id, protein_existence_type = self.pext, ecs = self.ecs)
