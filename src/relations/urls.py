from django.conf.urls import patterns, include, url

from relations.views import *
from relations.decorators import team_owner_only

urlpatterns = patterns('',
    url(r'team/add/$', add_team, name='add_team'),
    url(r'team/(?P<team_id>\d+)/edit/$', EditTeamView.as_view(), name='edit_team'),
    url(r'team/(?P<team_id>\d+)/', view_team, name='view_team'),
    url(r'$', view_contacts, name='view_contacts'),
)

