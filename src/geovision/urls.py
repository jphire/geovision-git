from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'userdb.views.loginpage'),
	(r'^login$', 'userdb.views.loginpage'),
	(r'^register$', 'userdb.views.register'),
	(r'^registering$', 'userdb.views.registering'),
	(r'^logging_in$', 'userdb.views.logging_in'),
	(r'^logging_out$', 'userdb.views.logging_out'),
	(r'^testgraph$', 'viz.views.testgraph'),
	(r'^graphrefresh$', 'viz.views.graphrefresh'),
	(r'^about$', 'userdb.views.about'),
	(r'^autocomplete$', 'viz.views.enzyme_autocompletion'),
	url(r'^admin/', include(admin.site.urls)),

	(r'', 'userdb.views.loginpage'), #everything else regirects to login for now
)
