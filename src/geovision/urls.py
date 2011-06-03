from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geovision.views.home', name='home'),
    # url(r'^geovision/', include('geovision.foo.urls')),
    (r'^$', 'userdb.views.login'), 
    (r'^login$', 'userdb.views.login'),
    (r'^register$', 'userdb.views.register'),
    (r'^registering$', 'userdb.views.registering'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'', 'userdb.views.login'), #everything else regirects to login for now
)
