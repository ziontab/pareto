from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # User accounts
    url(r'^login/$',    'parapp.views.login'),
    url(r'^register/$', 'parapp.views.register'),
    
    # Projects
    url(r'^projects/$', 'parapp.views.list_project'),
    url(r'^project/(?P<project_id>\d+)/$', 'parapp.views.get_project'),
    url(r'^ajax/project/create/$', 'parapp.views.create_projects'),

    # Calculations
    url(r'^calculations/(?P<project_id>\d+)/$', 'parapp.views.list_calculation'),
    url(r'^calculation/(?P<calculation_id>\d+)/$', 'parapp.views.get_calculation'),
    url(r'^calculation/create/$', 'parapp.views.create_calculation'),

    # Estimations
    url(r'^estimations/(?P<project_id>\d+)/$', 'parapp.views.list_estimation'),
    url(r'^estimation/(?P<estimation_id>\d+)/$', 'parapp.views.get_estimation'),
    url(r'^estimation/create/$', 'parapp.views.create_estimation'),

    # Admin
    url(r'^admin/',     include(admin.site.urls)),
)
