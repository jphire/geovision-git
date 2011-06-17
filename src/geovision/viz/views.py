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
    return render_to_response("graphviz.html", { }, context_instance=RequestContext(request) )
@login_required
def graphrefresh(request): #make a new JSon, set defaults if needed
    if request.POST['bitscore'] != '':
        bitscore = float(request.POST['bitscore'])
    else :
        bitscore = 20      #bitscore default
    if request.POST['e-value'] != '':
        evalue = float(request.POST['e-value'])
    else :
        evalue = 0.005        #e-value default
    if request.POST['depth'] != '':
        depth = float(request.POST['depth'])
    else :
        depth = 20         #depth default
    if request.POST['hits'] != '':
        hits = float(request.POST['hits'])
    else :
        hits = 10          #hits default
    setupderp()
    create_json(0, 0, "DB1", bitscore, evalue, depth, hits)
    return render_to_response("graphviz.html", { }, context_instance=RequestContext(request) )