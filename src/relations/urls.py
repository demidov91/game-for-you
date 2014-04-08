from django.conf.urls import patterns, include, url

from relations.views import *

urlpatterns = patterns('',
    url(r'team/add/$', add_team, name='add_team'),
    url(r'$', view_contacts, name='view_contacts'),
    url(r'team/(?P<team_id>\d+)/edit/$', edit_team, name='edit_team'),
)

