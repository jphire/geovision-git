#from geovision.text_to_db.create_JSON import create_json
from geovision.text_to_db.graph_JSON import QueryToJSON
from geovision.settings import PROJECT_PATH

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
from meta.models import EnzymeName, Enzyme
from geovision.viz.models import Blast
from geovision.settings import STATIC_URL
import json
import re
import urllib

def create_json(enzyme, read, dbentry, bitscore, evalue, depth, hits, offset):
	# for testing only
	qtj = QueryToJSON(enzyme, dbentry, read, evalue, bitscore, depth, hits, offset)

	return ('/graphjson?' + urllib.urlencode({ 'bitscore': bitscore, 'evalue': evalue, 'hits': hits}.items()),
					urllib.urlencode({'enzyme': enzyme or '', 'dbentry': dbentry or '', 'read': read or '', 'depth': depth, 'offset': offset}.items()))

# TODO: move somewhere else
def render(request, template, dict={}):
	user_settings = request.user.get_profile().settings
	return render_to_response(template, context_instance=RequestContext(request, merge_dict(dict, {'user_settings': user_settings})))
def merge_dict(d1, d2):
	d = {}
	d.update(d1)
	d.update(d2)
	return d


#Add '@login_required' to all these!
@login_required
def testgraph(request):
	return render_to_response("graphviz.html", {'enzyme':0, 'read':0, 'dbentry':'DB1', 'bitscore':30, 'evalue':0.005, 'depth':1, 'hits':10}, context_instance=RequestContext(request) )

@login_required
def graphjson(request):
	p = { 'bitscore': '', 'evalue': '', 'depth': '', 'hits': '', 'enzyme': '', 'read': '', 'dbentry': '', 'offset': '0'}
#	p = dict(map(lambda k: (k, request.GET[k]), ('enzyme', 'read', 'dbentry', 'bitscore', 'evalue', 'depth', 'hits')))
	for (k,v) in request.GET.items():
		p[k] = v
			
	for k in ('enzyme', 'read', 'dbentry'):
		if p[k] == '':
			p[k] = None
	try:
		out = QueryToJSON(p['enzyme'], p['dbentry'], p['read'], float(p['evalue']), float(p['bitscore']), int(p['depth']), int(p['hits']), int(p['offset']))
	except Exception as e:
		out = json.dumps({'error_message': str(e)})
	return HttpResponse(out, mimetype='text/plain')

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

	condition_dict = { 'bitscore': 30, 'evalue': 0.005, 'depth': 1, 'hits': 10, 'enzyme': '', 'read': '', 'dbentry': '', 'offset': 0}
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
	offset = int(condition_dict['offset'])

	json_url = ('', '')
	search_fields = filter(lambda k: condition_dict[k] != '', ['enzyme', 'read', 'dbentry'])
	if len(search_fields) > 1:
		return render(request, 'graphviz.html', merge_dict({
			'error_message': "Error: You can only enter one of the following: Enzyme, DB entry id, Read id.",
		}, condition_dict))
	if condition_dict['dbentry'] != '':
		json_url = create_json(None, None, condition_dict['dbentry'], bitscore, evalue, depth, hits, offset)
	elif condition_dict['enzyme'] != '':
		result = lookup_enzyme(condition_dict['enzyme'])
		if isinstance(result, basestring):
			json_url = create_json(result, None, None, bitscore, evalue, depth, hits, offset)
		elif result == None:
			return render(request, 'graphviz.html', merge_dict({'error_message': 'Enzyme not found'}, condition_dict))
		else: return render(request, 'graphviz.html', merge_dict(condition_dict, {'enzyme_list': result}))

	elif condition_dict['read']!='':
		json_url = create_json(None, condition_dict['read'], None, bitscore, evalue, depth, hits)
	if (json_url == 'error_no_children'):
		return render(request, 'graphviz.html', merge_dict({
			'error_message': "Error: No data found, input different values.",
		}, condition_dict))
	#c = Context ({enzyme:request.POST['enzyme'], read:request.POST['read'], dbentry:request.POST['dbentry'], bitscore:request.POST['bitscore'], evalue:request.POST['e-value'], depth:request.POST['depth'], hits:request.POST['hits']})
	(json_base_url, json_query_url_part) = json_url
	return render(request, "graphviz.html", merge_dict(condition_dict, {'json_base_url': json_base_url, 'json_query_url_part': json_query_url_part}))

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
		searchterm = request.GET['id']
	except KeyError:
		return HttpResponse('')
	data = Blast.objects.get(id = searchterm)
	return HttpResponse(json.dumps({'readseq': '%s' % (data.read_seq), 'dbseq': '%s' % (data.db_seq)}), mimetype='text/plain')

@login_required
def enzyme_data(request):
	try:
		searchterm = request.GET['id']
	except KeyError:
		return HttpResponse('')

	enzyme = Enzyme.objects.get(pk=searchterm)

	pathways = map(lambda x: {'id': x.id, 'name': x.name, 'enzymes': map(lambda y: y.pk, x.enzymes.all())}, enzyme.pathways.all())
	reactions = map(lambda x: {'id': x.id, 'name': x.name}, enzyme.reactions.all())
	names = map(lambda x: x.enzyme_name, EnzymeName.objects.filter(ec_number=searchterm).order_by('id'))

	return HttpResponse(json.dumps({'id': searchterm, 'names': names, 'pathways': pathways, 'reactions': reactions}), mimetype='text/plain')

