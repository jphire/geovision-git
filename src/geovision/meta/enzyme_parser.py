from viz.models import EnzymeName
from meta.models import Enzyme, Pathway
from meta.kegg_parser import *
from text_to_db.bulk_inserter import BulkInserter

def run(args):
	import sys
	ep = KeggParser(open(args[1], 'r'), ['ENTRY', 'NAME', 'PATHWAY'])
	name_inserter = BulkInserter(EnzymeName)

	while True:
		entry =  ep.get_entry()
		if not entry: break
		ecnum = entry['ENTRY'][0][3:14].strip()
		try:
			for name in entry['NAME']:
				name_inserter.save(EnzymeName(ec_number=ecnum, enzyme_name=name))
		except KeyError:
#			print('Warning, no names for EC %s' % (ecnum,))
			pass
		enzyme = Enzyme.objects.create(pk=ecnum)
		try:
			for pw in get_pathways(entry['PATHWAY']):
				enzyme.pathways.add(pw)

		except KeyError:
			pass
		enzyme.save()
	name_inserter.close()

if __name__ == '__main__':
	import sys
	run(sys.argv)
