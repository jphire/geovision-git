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

# TODO: move somewhere else
def render(request, template, dict={}):
	return render_to_response(template, context_instance=RequestContext(request, dict))


#Add '@login_required' to all these!
@login_required
def testgraph(request):
	return render_to_response("graphviz.html", {'ecnumber':0, 'read':0, 'dbentry':'DB1', 'bitscore':30, 'evalue':0.005, 'depth':1, 'hits':10}, context_instance=RequestContext(request) )
@login_required
def graphrefresh(request): #make a new JSon, set defaults if needed
	condition_dict = { 'bitscore': 30, 'evalue': 0.005, 'depth': 1, 'hits': 10 }
	for k in condition_dict.keys() + ['ecnumber', 'read', 'dbentry']:
		try:
			if request.POST[k] != '':
				condition_dict[k] = request.POST[k]
		except KeyError:
			pass
	error = ''
	if (request.POST['ecnumber']=='' and request.POST['read']=='' and request.POST['dbentry']!=''):
		error = create_json(0, 0, request.POST['dbentry'], bitscore, evalue, depth, hits)
	elif (request.POST['ecnumber']!='' and request.POST['read']=='' and request.POST['dbentry']==''):
			ec_numbers = EnzymeName.objects.filter(Q(enzyme_name__icontains=request.POST['ecnumber']) | Q(ec_number=request.POST['ecnumber']))
			num_results = len(ec_numbers)
			if num_results == 0: return render(request, 'graphviz.html', {'error_message': 'Enzyme not found'}.update(condition_dict))
			elif num_results == 1: error = create_json(ec_numbers[0].ec_number, 0, 0, bitscore, evalue, depth, hits)
			else: return render(request, graphviz.html, {'enzyme_list': ec_numbers}.update(condition_dict))

	elif (request.POST['ecnumber']=='' and request.POST['read']!='' and request.POST['dbentry']==''):
		error = create_json(0, request.POST['read'], 0, bitscore, evalue, depth, hits)
	else:
		return render(request, 'graphviz.html', {
			'error_message': "Error: You can only enter one of the following: Enzyme, DB entry id, Read id.",
		}.update(condition_dict))
	if (error == 'error_no_children'):
		return render(request, 'graphviz.html', {
			'error_message': "Error: No data found, input different values.",
		}.update(condition_dict))
	#c = Context ({ecnumber:request.POST['ecnumber'], read:request.POST['read'], dbentry:request.POST['dbentry'], bitscore:request.POST['bitscore'], evalue:request.POST['e-value'], depth:request.POST['depth'], hits:request.POST['hits']})
	return render(request, "graphviz.html", condition_dict)