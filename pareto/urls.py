from django.conf.urls import patterns, include, url
from django.contrib import admin
from parapp.models import Project, Calculation, Estimation, Analysis, Problem, Algorithm, Indicator

admin.autodiscover()

urlpatterns = patterns('',
    # User accounts
    url(r'^$',          'parapp.views.get_main'),
    url(r'^login/$',    'parapp.views.login'),
    url(r'^logout/$',   'parapp.views.logout'),
    url(r'^register/$', 'parapp.views.register'),
    
    # Projects
    url(r'^projects/$',                                'parapp.views.list_project'),
    url(r'^project/(?P<project_id>\d+)/$',             'parapp.views.get_project'),
    url(r'^ajax/project/create/$',                     'parapp.views.create_project'),
    url(r'^ajax/project/edit/(?P<project_id>\d+)/$',   'parapp.views.edit_project'),
    url(r'^ajax/project/delete/(?P<project_id>\d+)/$', 'parapp.views.delete_project'),
    url(r'^ajax/project_row/$',                        'parapp.views.list_project_row'),
    url(r'^ajax/project_search/$',                     'parapp.views.search_project'),

    # Estimations
    url(r'^estimation/(?P<estimation_id>\d+)/$',      'parapp.views.get_estimation'),
    url(r'^estimation/create/(?P<project_id>\d+)/$',  'parapp.views.create_estimation'),
    url(r'^ajax/estimation/(?P<estimation_id>\d+)/$', 'parapp.views.get_estimation'),
    url(r'^ajax/estimation/delete/(?P<id>\d+)/$',     'parapp.views.delete_entity', {"entity" : Estimation}),
    url(r'^ajax/estimation/start/(?P<id>\d+)/$',      'parapp.views.start_entity', {"entity" : Estimation}),

    # Calculations
    url(r'^calculation/(?P<calculation_id>\d+)/$',      'parapp.views.get_calculation'),
    url(r'^calculation/create/(?P<project_id>\d+)/$',   'parapp.views.create_calculation'),
    url(r'^ajax/calculation/(?P<calculation_id>\d+)/$', 'parapp.views.get_calculation'),
    url(r'^ajax/calculation/delete/(?P<id>\d+)/$',      'parapp.views.delete_entity', {"entity" : Calculation}),
    url(r'^ajax/calculation/start/(?P<id>\d+)/$',       'parapp.views.start_entity', {"entity" : Calculation}),

    # Analyzes
    url(r'^analysis/(?P<analysis_id>\d+)/$',       'parapp.views.get_analysis'),
    url(r'^analysis/create/(?P<project_id>\d+)/$', 'parapp.views.create_analysis'),
    url(r'^ajax/analysis/(?P<analysis_id>\d+)/$',  'parapp.views.get_analysis'),
    url(r'^ajax/analysis/delete/(?P<id>\d+)/$',    'parapp.views.delete_entity', {"entity" : Analysis}),
    url(r'^ajax/analysis/start/(?P<id>\d+)/$',    'parapp.views.start_entity', {"entity" : Analysis}),

    # API
    url(r'^api_back/$', 'parapp.views.api_back'),
    url(r'^new_calc/$', 'parapp.views.stub'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
