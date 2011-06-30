from geovision.text_to_db.create_JSON import create_json
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
import re

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
	def lookup_enzyme(enzyme):
		match = re.search("\\(([-0-9.]+)\\)", enzyme) # XXX: queries of form 'asdasdasd (1.2.3.4) return 1.2.3.4 with all values of asdasdasd
		if match:
			enzyme = match.group(1)

		ec_match = EnzymeName.objects.filter(ec_number=enzyme).exists()
		if ec_match:
			return enzyme
		else:
			ec_numbers = EnzymeName.objects.filter(enzyme_name__iexact=enzyme)
			num_results = len(ec_numbers)
			if num_results == 0: return None
			elif num_results == 1: return enzyme.ec_number
			else: return ec_numbers

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
		result = lookup_enzyme(condition_dict['ecnumber'])
		if isinstance(result, basestring):
			error = create_json(result, 0, 0, bitscore, evalue, depth, hits)
		elif result == None:
			return render(request, 'graphviz.html', merge_dict({'error_message': 'Enzyme not found'}, condition_dict))
		else: return render(request, 'graphviz.html', merge_dict(condition_dict, {'enzyme_list': result}))

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

	matches = EnzymeName.objects.filter(enzyme_name__istartswith=search).order_by('enzyme_name')[:limit]
	return HttpResponse(json.dumps([{'label': '%s (%s)' % (en.enzyme_name, en.ec_number)} for en in matches]), mimetype='text/plain')
@login_required
def show_alignment(request):
	try:
		search = request.GET['term']
	except KeyError:
		return HttpResponse('')
	#	Blastin read_seq = models.TextField()
	#   db_seq = models.TextField()
	alignment = Blast.objects.filter(enzyme_name__istartswith=search).order_by('enzyme_name')
	return HttpResponse(json.dumps([{'label': '%s (%s)' % (en.enzyme_name, en.ec_number)} for en in matches]), mimetype='text/plain')
