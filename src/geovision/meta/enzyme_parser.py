from meta.models import Enzyme, Pathway, EnzymeName
from meta.kegg_parser import *
from text_to_db.bulk_inserter import BulkInserter
import sys

def run(args):
	ep = KeggParser(open(args[1], 'r'), ['ENTRY', 'NAME', 'PATHWAY', 'CLASS'])
	name_inserter = BulkInserter(EnzymeName)

	try:
		while True:
			entry = ep.get_entry()
			if not entry: break
			ecnum = entry['ENTRY'][0][3:14].strip()
	
			try:
				namesrc = entry['NAME']
			except KeyError:
				namesrc = entry['CLASS']
			for name in namesrc:
				name_inserter.save(EnzymeName(ec_number=ecnum, enzyme_name=name))
			enzyme = Enzyme.objects.create(pk=ecnum)
			try:
				for pw in get_pathways(entry['PATHWAY']):
					enzyme.pathways.add(pw)
	
			except KeyError:
				pass
			enzyme.save()
		name_inserter.close()
	except Exception:
		name_inserter.rollback()

if __name__ == '__main__':
	run(sys.argv)
