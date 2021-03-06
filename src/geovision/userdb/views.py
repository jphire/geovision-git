from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import json
from userdb.models import SavedView


def loginpage(request):
	"""
	Redirects authenticated users straight in and shows the login form for the rest.
	"""

	if request.user.is_authenticated():
		return redirect('/graphrefresh')
	else:
		return render_to_response("login.html", { }, context_instance=RequestContext(request) )

def register(request):
	"""
	Shows the page with the registering form.
	"""
	return render_to_response("register.html", { }, context_instance = RequestContext(request) )


def registering(request):
	"""
	Registers a new user, is called from the registering page.
	"""
	datatable = [request.POST['username'], request.POST['email'], request.POST['password1'], request.POST['password2']]
	for data in datatable: #checks to see that all fields have data
		if (len(data) < 1):
			return render_to_response('register.html', {
			'error_message': "Error: All fields must be filled.",
		}, context_instance=RequestContext(request)) #error message for for not filling all fields!
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
		#new account created - note: it must be activated via the admin panel to be fully functional


def logging_in(request):
	"""
	Logs a user in, is called from the login page.
	"""
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password) #djangos auth
	if user is not None:
		if user.is_active: #user has to be active to log in
			login(request, user)
			return redirect('/graphrefresh')
		else:
			return render_to_response('login.html', { #error for a not activated account
					'error_message': "Account is not active.",
					}, context_instance = RequestContext(request))
	else:
		return render_to_response('login.html', { #login for incorrect username and/or password
			'error_message': "Username or password was incorrect.",
		}, context_instance = RequestContext(request))

def logging_out(request):
	"""
	Logs the user out. Is called from the logout -button.
	"""
	logout(request)
	return redirect('/')

@login_required
def savesettings(request):
	"""
	Saves the user's settings.
	"""
	profile = request.user.get_profile()
	if 'defaultsettings' not in request.POST:
		duration = request.POST['duration']
		canvas_x = request.POST['canvas_x']
		canvas_y = request.POST['canvas_y']
		type = ''
		transition = ''
		if request.POST['group1'] == 'animations_off':
			type = 'replot'
		else:
				type = 'fade:con'
		transition = request.POST['animationtype']
		subtype = request.POST['animationsubtype']

		settings = json.dumps({'settings': {'canvaswidth': canvas_x, 'canvasheight': canvas_y}, 'animationsettings': {'type': type, 'duration': duration, 'subtype': subtype, 'transition': transition}})
		#makes a json out of the settings and saves it
		profile.settings = settings
		profile.save()
		return HttpResponse('Settings saved', mimetype='text/plain')
	else:
		profile.settings = '{}'
		profile.save()
		return HttpResponse('Restored defaults', mimetype='text/plain')

@login_required
def save_view(request):
	"""
	Saves the graph the user was looking at.
	"""
	profile = request.user.get_profile()
	id_to_delete = request.GET.get('delete')
	if id_to_delete:
		try:
			profile.saved_views.get(pk=id_to_delete).delete()
		except SavedView.DoesNotExist:
			pass
		return HttpResponseRedirect('/graphrefresh')
	view = profile.saved_views.create(name=request.POST['name'], graph=request.POST['graph'], query=request.POST['query'])
	return HttpResponse(str(view.id))

@login_required
def export_view(request):
	"""
	Fetches the requested saved graph view and returns it as json.
	"""
	type = request.GET.get('type', 'json')
	id = int(request.GET['id'])

	view = request.user.get_profile().saved_views.get(pk=id)
	graph_json = view.graph
	content = None

	if type == 'json':
		content = graph_json
	else:
		content = 'Invalid "type" argument to export_view'

	return HttpResponse(content, mimetype='text/plain')


