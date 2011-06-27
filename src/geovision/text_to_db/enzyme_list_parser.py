from geovision.text_to_db.bulk_inserter import *
from geovision.viz.models import EnzymeName

class enzyme_parser:
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

if __name__ == '__main__':
	import sys
	ep = enzyme_parser(open(sys.argv[1], 'r'), ['ENTRY', 'NAME'])
	inserter = BulkInserter(EnzymeName)

	while True:
		entry =  ep.get_entry()
		if not entry: break
		ecnum = entry['ENTRY'][0][3:13].strip()
		try:
			for name in entry['NAME']:
				inserter.save(EnzymeName(ec_number=ecnum, enzyme_name=name))
		except KeyError:
			print('Warning, no names for EC %s' % (ecnum,))

	inserter.close()
