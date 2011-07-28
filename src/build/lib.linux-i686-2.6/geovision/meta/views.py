from django.http import HttpResponse
from meta.models import Pathway
from viz.views import render
import json
from geovision.settings import STATIC_URL

def metaboly_json(request):
	pwid = request.GET['pathway']
	pathway = Pathway.objects.get(pk=pwid)

	compounds = pathway.compounds.all()
	c_ids = map(lambda c: c.id, compounds)
	reactions = pathway.reactions.all()
	r_ids = map(lambda r: r.id, reactions)

	result = []
	for c in compounds:
		c_dict = {'id': c.id, 'adjacencies': [], 'data': {'name': c.name}}
		result.append(c_dict)

		for reac in c.reactant_reactions.all():
			if False or reac.id in r_ids:
				c_dict['adjacencies'].append({'nodeTo': reac.id})
	for reac in reactions:
		r_dict = {'id': reac.id, 'adjacencies': [], 'data': {'name': ','.join((e.ec_number for e in reac.enzymes.all()))}}
		result.append(r_dict)
		for c in reac.products.all():
			if False or c.id in c_ids:
				r_dict['adjacencies'].append({'nodeTo': c.id})
	return HttpResponse(json.dumps(result,indent=True), mimetype='text/plain')

def show_metaboly(request):
	pathway_id = request.GET['pathway']
	return render(request, 'show_metaboly.html', { 'pathway_id': pathway_id })
