from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geovision.views.home', name='home'),
    # url(r'^geovision/', include('geovision.foo.urls')),
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
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'', 'userdb.views.loginpage'), #everything else regirects to login for now
)
