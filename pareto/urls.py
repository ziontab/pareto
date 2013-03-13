from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$',    'parapp.views.login'),
    url(r'^register/$', 'parapp.views.register'),
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^$', 'pareto.views.home', name='home'),
    # url(r'^pareto/', include('pareto.foo.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
