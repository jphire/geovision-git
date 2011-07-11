from geovision.text_to_db.bulk_inserter import *

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

