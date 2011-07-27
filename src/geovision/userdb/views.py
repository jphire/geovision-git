from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 

def loginpage(request):
	if request.user.is_authenticated():
		return redirect('/graphrefresh')
	else:
		return render_to_response("login.html", { }, context_instance=RequestContext(request) )
def register(request):
	return render_to_response("register.html", { }, context_instance=RequestContext(request) )

def registering(request):
	datatable = [request.POST['username'], request.POST['email'], request.POST['password1'], request.POST['password2']]
	for data in datatable:
		if (len(data) < 1):
			return render_to_response('register.html', {
			'error_message': "Error: All fields must be filled.",
		}, context_instance=RequestContext(request)) #error for for not filling all fields!
	if (cmp(request.POST['password1'], request.POST['password2']) != 0 ):
		return render_to_response('register.html', {
			'error_message': "Error: Passwords did not match.",
		}, context_instance=RequestContext(request)) #error for entering two different passwords!
	user, new = User.objects.get_or_create(username = request.POST['username'])
	if (new == False):
		return render_to_response('register.html', {
			'error_message': "Error: User already exists.",
		}, context_instance=RequestContext(request)) #error trying the same username two times!
	else:
		user.set_password(request.POST['password2'])
		user.email = request.POST['email']
		user.is_staff = False
		user.is_active = False
		user.save()
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
			return redirect('/graphrefresh')
		else:
			return render_to_response('login.html', {
					'error_message': "Account is not active.",
					}, context_instance=RequestContext(request))
	else:
		return render_to_response('login.html', {
			'error_message': "Username or password was incorrect.",
		}, context_instance=RequestContext(request))

def logging_out(request):
	logout(request)
	return redirect('/')

def about(request):
	return render_to_response("about.html")
@login_required
def savesettings(request):
		profile = request.user.get_profile()
		numericsMakeSense = False;
		if (request.POST['canvas_x'].isdigit() and request.POST['canvas_y'].isdigit() and request.POST['duration'].isdigit()):
			numericsMakeSense = True;
		if 'savesettings' in request.POST and numericsMakeSense:
			type = ''
			transition = ''
			if request.POST['group1']==animation_on:
				type = 'animate'
			else:
				type = 'replot'
			if request.POST['animationtype']=='linear':
				transition = '$jit.Trans.linear'
			else:
				transition = '$jit.Trans.'+'request.POST["animationtype"]'+'.'+'request.POST["animationsubtype"]'
			settings = json.dumps({'settings': {'canvaswidth': request.POST['canvas_x'], 'canvasheight': request.POST['canvas_y']}, 'animationsettings': {'type': type, 'duration': request.POST['duration'], 'transition': transition}})
			profile.settings = settings
			profile.save()
			return redirect('graphrefresh?settingsmessage="settings saved"')
		elif 'defaultsettings' in request.POST:
			profile.settings = '{}'
			profile.save()
			return HttpResponseRedirect(reverse('graphrefresh', kwargs={'settingsmessage': "defaults restored"}))
		else:
			return redirect('graphrefresh?settingsmessage="error"')