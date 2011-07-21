from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

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
	(r'^about$', 'userdb.views.about'),

	(r'^testgraph$', 'viz.views.testgraph'),
	(r'^graphrefresh$', 'viz.views.graphrefresh'),
	(r'^graphjson$', 'viz.views.graphjson'),
	(r'^show_alignment$', 'viz.views.show_alignment'),
	(r'^autocomplete$', 'viz.views.enzyme_autocompletion'),
	(r'^enzyme_names$', 'viz.views.enzyme_names'),

	(r'^metaboly_json$', 'meta.views.metaboly_json'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	(r'', 'userdb.views.loginpage'), #everything else regirects to login for now
)
