# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

def login(request):
    return render_to_response("login.html", { }, context_instance=RequestContext(request) )
def register(request):
    return render_to_response("register.html", { }, context_instance=RequestContext(request) )
def registering(request):
    if (cmp(request.POST['password1'], request.POST['password2']) != 0 ):
        return render_to_response('register.html', {
            'error_message': "Error: Passwords did not match.",
        }, context_instance=RequestContext(request)) #error for entering two different passwords!
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password2'])
    user.is_staff = False
    user.save()
    #TODO: check safety and lenghts!!!
    return render_to_response('login.html', {
            'error_message': "Account succesfully created.",
        }, context_instance=RequestContext(request)) 
