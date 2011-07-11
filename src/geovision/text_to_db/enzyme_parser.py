from viz.models import EnzymeName, Enzyme, Pathway
from text_to_db.kegg_parser import *
from text_to_db.bulk_inserter import BulkInserter

def run(args):
	import sys
	ep = KeggParser(open(args[1], 'r'), ['ENTRY', 'NAME', 'PATHWAY'])
	name_inserter = BulkInserter(EnzymeName)
	enzyme_inserter = BulkInserter(Enzyme)

	while True:
		entry =  ep.get_entry()
		if not entry: break
		ecnum = entry['ENTRY'][0][3:13].strip()
		try:
			for name in entry['NAME']:
				name_inserter.save(EnzymeName(ec_number=ecnum, enzyme_name=name))
		except KeyError:
#			print('Warning, no names for EC %s' % (ecnum,))
			pass
		enzyme = Enzyme()
		try:
			for pathway in entry['PATHWAY']:
				id = pathway[2:7]
				name = pathway[9:]
				try:
					pw = Pathway.objects.get(pk=id)
				except Pathway.DoesNotExist:
					pw = Pathway.create(pk=id, name=name)
				enzyme.pathways += pw
		except:
			pass
		enzyme_inserter.save(enzyme)
	name_inserter.close()

if __name__ == '__main__':
	import sys
	run(sys.argv)