# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf

def loginpage(request):
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
def logging_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response("graphviz.html", { }, context_instance=RequestContext(request) )
        else:
            return render_to_response('login.html', {
                    'error_message': "Account is not active.",
                    }, context_instance=RequestContext(request))
    else:
        return render_to_response('login.html', {
            'error_message': "The username or password was incorrect.",
        }, context_instance=RequestContext(request))

def logging_out(request):
    logout(request)
    return render_to_response("login.html", {'error_message': "You have been logged out.", }, context_instance=RequestContext(request) )

#graphviews moved to viz.views