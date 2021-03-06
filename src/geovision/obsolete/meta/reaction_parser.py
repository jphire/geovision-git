from meta.models import Reaction, Enzyme
from meta.kegg_parser import *
import re

COMPOUND_REGEX = re.compile(r'C[0-9]{5}')

def extract_compounds(equ):
	sides = equ.split('<=>')
	words = map(lambda x: x.split(), sides)
	return map(lambda x: filter(COMPOUND_REGEX.match, x), words)

def run(args):
	import sys
	ep = KeggParser(open(args[1], 'r'), ['ENTRY', 'NAME', 'EQUATION', 'ENZYME', 'DEFINITION', 'PATHWAY'])

	while True:
		entry =  ep.get_entry()
		if not entry: break

		rnum = entry['ENTRY'][0][1:6].strip()
		equ = entry['EQUATION'][0]

		try:
			enzyme = entry['ENZYME'][0]
		except KeyError:
			enzyme = ''

		try:
			name = entry['NAME'][0]
		except KeyError:
			name = entry['DEFINITION'][0]
		reaction = Reaction.objects.create(pk=rnum, name=name) #, equation=entry['DEFINITION'][0])
		reaction.enzymes = Enzyme.objects.filter(pk__in=enzyme.split())

		try:
			for pw in get_pathways(entry['PATHWAY']):
				reaction.pathways.add(pw)

		except KeyError:
			pass

		(reactants, products) = extract_compounds(equ)
		reaction.reactants = map(lambda x: x[1:6], reactants)
		reaction.products = map(lambda x: x[1:6], products)

		reaction.save()

if __name__ == '__main__':
	import sys
	run(sys.argv)
