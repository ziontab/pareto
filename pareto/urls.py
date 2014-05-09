from django.conf.urls import patterns, include, url
from django.contrib import admin

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

    # API
    url(r'^api_back/$', 'parapp.views.api_back'),
    url(r'^new_calc/$', 'parapp.views.stub'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
