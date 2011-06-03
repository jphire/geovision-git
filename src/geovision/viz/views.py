# Create your views here.
def testgraph(request):
    return render_to_response("graphviz.html", { }, context_instance=RequestContext(request) )