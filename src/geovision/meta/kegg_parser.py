from geovision.text_to_db.bulk_inserter import *
from meta.models import Pathway

class KeggParser:
	def __init__(self, filehandle, fields):
		self.filehandle = filehandle
		self.fields = fields

	@classmethod
	def split(cls, line):
		return (line[:12].strip(), line[12:].rstrip(";\n"))

	def get_entry(self):
		entry = {}
		cur_key = None
		cur_valuelist = []
		for line in self.filehandle:
			(key, value) = self.split(line)
			if key == '///':
				return entry
			if key != '':
				cur_key = key if key in self.fields else None

				if cur_key:
					cur_valuelist = []
					entry[key] = cur_valuelist
			if cur_key:
				cur_valuelist.append(value)
		return None

def get_pathways(entry):
	i = 0
	elems = []
	while i < len(entry):
		pw = entry[i]
		while i+1 < len(entry) and entry[i+1].startswith(' '):
			pw += ' ' + entry[i+1].lstrip()
			i += 1
		(id, name) = pw.split(None, 1)
		id = filter(str.isdigit, id)
		pwobj = Pathway.objects.get_or_create(id=id, name=name)[0]
		pwobj.save()
		elems.append(pwobj)
		i += 1
	return elems
		
