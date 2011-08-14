from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
from geovision.admin import setup_admin
setup_admin()

urlpatterns = patterns('',
	(r'^$', 'userdb.views.loginpage'),
	(r'^login$', 'userdb.views.loginpage'),
	(r'^register$', 'userdb.views.register'),
	(r'^registering$', 'userdb.views.registering'),
	(r'^logging_in$', 'userdb.views.logging_in'),
	(r'^logging_out$', 'userdb.views.logging_out'),
	(r'^about$', direct_to_template, { 'template': 'about.html'}),
	(r'^show_help$', direct_to_template, { 'template': 'help.html'}),
	(r'^qunit$', direct_to_template, { 'template': 'qunit.html'}),

	(r'^savesettings$', 'userdb.views.savesettings'),
	(r'^save_view$', 'userdb.views.save_view'),
	(r'^export_view$', 'userdb.views.export_view'),

	(r'^graphrefresh$', 'viz.views.graphrefresh'),
	(r'^graphjson$', 'viz.views.graphjson'),
	(r'^show_alignment$', 'viz.views.show_alignment'),
	(r'^autocomplete$', 'viz.views.enzyme_autocompletion'),

	(r'^enzyme_data$', 'viz.views.enzyme_data'),

	(r'^admin/', include(admin.site.urls)),

)
urlpatterns += staticfiles_urlpatterns()
