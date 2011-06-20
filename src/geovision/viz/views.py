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

#Add '@login_required' to all these!
@login_required
def testgraph(request):
    return render_to_response("graphviz.html", {ecnumber:0, read:0, dbentry:'DB1', bitscore:30, evalue:0.005, depth:1, hits:10}, context_instance=RequestContext(request) )
@login_required
def graphrefresh(request): #make a new JSon, set defaults if needed
    if request.POST['bitscore'] != '':
        bitscore = float(request.POST['bitscore'])
    else :
        bitscore = 30      #bitscore default
    if request.POST['e-value'] != '':
        evalue = float(request.POST['e-value'])
    else :
        evalue = 0.005        #e-value default
    if request.POST['depth'] != '':
        depth = float(request.POST['depth'])
    else :
        depth = 1         #depth default
    if request.POST['hits'] != '':
        hits = float(request.POST['hits'])
    else :
        hits = 10          #hits default
    error = ''
    if (request.POST['ecnumber']=='' and request.POST['read']=='' and request.POST['dbentry']!=''):
        error = create_json(0, 0, request.POST['dbentry'], bitscore, evalue, depth, hits)
    elif (request.POST['ecnumber']!='' and request.POST['read']=='' and request.POST['dbentry']==''):
        error = create_json(request.POST['ecnumber'], 0, 0, bitscore, evalue, depth, hits)
    elif (request.POST['ecnumber']=='' and request.POST['read']!='' and request.POST['dbentry']==''):
        error = create_json(0, request.POST['read'], 0, bitscore, evalue, depth, hits)
    else:
        return render_to_response('graphviz.html', {
            'error_message': "Error: You can only enter one of the following: ECnumber, DB entry id, Read id.",
        }, context_instance=RequestContext(request))
    if (error == 'error_no_children'):
        return render_to_response('graphviz.html', {
            'error_message': "Error: No data found, input different values.",
        }, context_instance=RequestContext(request))
    #c = Context ({ecnumber:request.POST['ecnumber'], read:request.POST['read'], dbentry:request.POST['dbentry'], bitscore:request.POST['bitscore'], evalue:request.POST['e-value'], depth:request.POST['depth'], hits:request.POST['hits']})
    return render_to_response("graphviz.html", {ecnumber:request.POST['ecnumber'], read:request.POST['read'], dbentry:request.POST['dbentry'], bitscore:request.POST['bitscore'], evalue:request.POST['e-value'], depth:request.POST['depth'], hits:request.POST['hits']}, context_instance=RequestContext(request) )