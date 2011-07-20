from meta.models import Compound, Pathway
from text_to_db.kegg_parser import *

def run(args):
	import sys
	ep = KeggParser(open(args[1], 'r'), ['ENTRY', 'NAME', 'PATHWAY'])

	while True:
		entry =  ep.get_entry()
		if not entry: break
		cnum = entry['ENTRY'][0][1:6].strip()

		compound = Compound.objects.create(pk=cnum, name=entry['NAME'][0])
		try:
			for pw in get_pathways(entry['PATHWAY']):
				compound.pathways.add(pw)

		except KeyError:
			pass
		compound.save()

if __name__ == '__main__':
	import sys
	run(sys.argv)
