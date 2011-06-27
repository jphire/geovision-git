# Create your views here.
from geovision.text_to_db.create_JSON import create_json
from geovision.text_to_db.create_JSON import setupderp #TEMP
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.db.models import Q
from geovision.viz.models import EnzymeName
import json

# TODO: move somewhere else
def render(request, template, dict={}):
	return render_to_response(template, context_instance=RequestContext(request, dict))
def merge_dict(d1, d2):
	d = {}
	d.update(d1)
	d.update(d2)
	return d


#Add '@login_required' to all these!
@login_required
def testgraph(request):
	return render_to_response("graphviz.html", {'ecnumber':0, 'read':0, 'dbentry':'DB1', 'bitscore':30, 'evalue':0.005, 'depth':1, 'hits':10}, context_instance=RequestContext(request) )
@login_required
def graphrefresh(request): #make a new JSon, set defaults if needed
	condition_dict = { 'bitscore': 30, 'evalue': 0.005, 'depth': 1, 'hits': 10, 'ecnumber': '', 'read': '', 'dbentry': ''}
	for k in condition_dict.keys():
		try:
			if request.POST[k] != '':
				condition_dict[k] = request.POST[k]
		except KeyError:
			pass
	bitscore = float(condition_dict['bitscore'])
	evalue = float(condition_dict['evalue'])
	depth = int(condition_dict['depth'])
	hits = int(condition_dict['hits'])

	error = ''
	search_fields = filter(lambda k: condition_dict[k] != '', ['ecnumber', 'read', 'dbentry'])
	if len(search_fields) > 1:
		return render(request, 'graphviz.html', merge_dict({
			'error_message': "Error: You can only enter one of the following: Enzyme, DB entry id, Read id.",
		}, condition_dict))
	if condition_dict['dbentry'] != '':
		error = create_json(0, 0, condition_dict['dbentry'], bitscore, evalue, depth, hits)
	elif condition_dict['ecnumber']!='':
			ec_match = EnzymeName.objects.filter(ec_number=condition_dict['ecnumber']).exists()
			if ec_match:
				error = create_json(condition_dict['ecnumber'], 0, 0, bitscore, evalue, depth, hits)
			else:
				ec_numbers = EnzymeName.objects.filter(enzyme_name__iexact=condition_dict['ecnumber'])
				num_results = len(ec_numbers)
				if num_results == 0: return render(request, 'graphviz.html', merge_dict({'error_message': 'Enzyme not found'}, condition_dict))
				elif num_results == 1: error = create_json(ec_numbers[0].ec_number, 0, 0, bitscore, evalue, depth, hits)
				else: return render(request, 'graphviz.html', merge_dict(condition_dict, {'enzyme_list': ec_numbers}))

	elif condition_dict['read']!='':
		error = create_json(0, condition_dict['read'], 0, bitscore, evalue, depth, hits)
	if (error == 'error_no_children'):
		return render(request, 'graphviz.html', merge_dict({
			'error_message': "Error: No data found, input different values.",
		}, condition_dict))
	#c = Context ({ecnumber:request.POST['ecnumber'], read:request.POST['read'], dbentry:request.POST['dbentry'], bitscore:request.POST['bitscore'], evalue:request.POST['e-value'], depth:request.POST['depth'], hits:request.POST['hits']})
	return render(request, "graphviz.html", condition_dict)

	@login_required
	def enzyme_autocompletion(request):
		try:
			search = request.GET['term']
		except KeyError:
			return HttpResponse('')
		try:
			limit = request.GET['limit']
		except KeyError:
			limit = 10

		matches = EnzymeName.objects.filter(enzyme_name__startswith=search).order_by('enzyme_name')[:limit]
		return HttpResponse(json.dump(({'id': en.ec_number, 'label': '%s (%s)' % (en.enzyme_name, en.ec_number)} for en in matches)))
