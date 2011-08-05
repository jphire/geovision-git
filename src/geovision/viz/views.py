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
from geovision.userdb.models import Sample
from geovision.settings import STATIC_URL
import json
import re
import urllib

def render(request, template, dict={}):
	profile = request.user.get_profile()
	return render_to_response(template, context_instance=RequestContext(request, merge_dict(dict, {'user_settings': profile.settings, 'saved_views': profile.saved_views.all(), 'settingsmessage': request.GET.get('settingsmessage')})))

def merge_dict(d1, d2):
	"""
	Merges two dictionaries given as arguments. The latter one overwrites the former.
	"""
	d = {}
	d.update(d1)
	d.update(d2)
	return d

#Add '@login_required' to all these!
@login_required
def graphjson(request):
	p = { 'bitscore': '', 'evalue': '', 'depth': '', 'hits': '', 'enzyme': '', 'read': '', 'dbentry': '', 'offset': '0', 'samples':[]}

	for (k,v) in request.GET.items():
		p[k] = v
			
	view_id = request.GET.get('view_id')
	if view_id:
		return HttpResponse(request.user.get_profile().saved_views.get(pk=int(view_id)).graph, mimetype='text/plain')
	for k in ('enzyme', 'read', 'dbentry'):
		if p[k] == '':
			p[k] = None

	p['samples'] = request.GET.getlist('samples[]')
	try:
		out = QueryToJSON(p['enzyme'], p['dbentry'], p['read'], float(p['evalue']), float(p['bitscore']), int(p['depth']), int(p['hits']), float(p['offset']), p['samples'])
	except Exception as e:
		out = json.dumps({'error_message': str(e)})
	return HttpResponse(out, mimetype='text/plain')

@login_required
def graphrefresh(request): #make a new JSon, set defaults if needed
	def lookup_enzyme(enzyme):
		match = re.search('^\s*(.*?)\s*\(([-0-9.]+)\)\s*$', enzyme)
		enzyme_name = None
		if match:
			enzyme = match.group(2)
			enzyme_name = match.group(1)

		ec_match = EnzymeName.objects.filter(ec_number=enzyme)
		if enzyme_name: ec_match.filter(enzyme_name=enzyme_name)
		if ec_match.exists():
			return [enzyme]
		else:
			ec_numbers = EnzymeName.objects.filter(enzyme_name__iexact=enzyme)
			return ec_numbers

	def get_samples():
		samples = []
		sample_collection = Sample.objects.all()
		for sample in sample_collection:
			samples.append(sample.sample_id)
		return samples

	condition_dict = { 'bitscore': 30, 'evalue': 0.005, 'depth': 1, 'hits': 5, 'enzyme': '', 'read': '', 'dbentry': '', 'offset': 0}
	view_id = request.GET.get('open_view')
	if view_id:
		saved_view = request.user.get_profile().saved_views.defer('graph').get(pk=view_id)
		condition_dict['view_id'] = view_id
		return render(request, 'graphviz.html', merge_dict(condition_dict, json.loads(saved_view.query)))

	for k in condition_dict.keys():
		try:
			if request.POST[k] not in ('', []):
				condition_dict[k] = request.POST[k]
		except KeyError:
			pass
	samples = request.POST.getlist('samples')
	condition_dict['samples'] = samples
	all_samples = get_samples()
	condition_dict['all_samples'] = all_samples

	if samples == []:
		samples = all_samples
		condition_dict['samples'] = all_samples

	search_fields = filter(lambda k: condition_dict[k] != '', ['enzyme', 'read', 'dbentry'])
	if len(search_fields) > 1:
		return render(request, 'graphviz.html', merge_dict({
			'error_message': "Error: You can only enter one of the following: Enzyme, DB entry id, Read id.",
		}, condition_dict))

	elif condition_dict['enzyme'] != '':
		if len(result) == 1:
			condition_dict['enzyme'] = result[0] if isinstance(result[0], basestring) else result[0].ec_number
		elif result == None:
			return render(request, 'graphviz.html', merge_dict({'error_message': 'Enzyme not found'}, condition_dict))
		else:
			return render(request, 'graphviz.html', merge_dict(condition_dict, {'enzyme_list': result}))

	return render(request, "graphviz.html", condition_dict)

@login_required
def enzyme_autocompletion(request):
	try:
		search = request.GET['term']
	except KeyError:
		return HttpResponse('')

	matches = EnzymeName.objects.filter(enzyme_name__istartswith=search).order_by('enzyme_name')[:10]
	return HttpResponse(json.dumps([{'label': '%s (%s)' % (en.enzyme_name, en.ec_number)} for en in matches]), mimetype='text/plain')

@login_required
def show_alignment(request):
	try:
		searchterm = request.GET['id']
	except KeyError:
		return HttpResponse('')
	data = Blast.objects.get(id=searchterm)
	return HttpResponse(json.dumps({'readseq': '%s' % (data.read_seq), 'dbseq': '%s' % (data.db_seq)}), mimetype='text/plain')

@login_required
def enzyme_data(request):
	try:
		searchterm = request.GET['id']
	except KeyError:
		return HttpResponse('')
	enzyme = Enzyme.objects.get(pk=searchterm)

	pathways = map(lambda x: {'id': x.id, 'name': x.name, 'enzymes': map(lambda y: y.pk, x.enzymes.all())}, enzyme.pathways.all())
	names = map(lambda x: x.enzyme_name, EnzymeName.objects.filter(ec_number=searchterm).order_by('id'))

	return HttpResponse(json.dumps({'id': searchterm, 'names': names, 'pathways': pathways}), mimetype='text/plain')
