from django.conf.urls import patterns, include, url

from relations.views import *
from relations.decorators import team_owner_only

urlpatterns = patterns('',


    url(r'ajax/people/find/name/contains/', find_by_name, name='find_people_by_name'),
    url(r'ajax/contact/add/', add_contact, name='add_contact'),
    url(r'ajax/contact/(?P<contact_id>\d+)/remove/', remove_contact, name='remove_contact'),
    url(r'ajax/team/(?P<team_id>\d+)/member/add/(?P<userprofile_id>\d+)/', add_team_member, name='add_team_member'),
    url(r'ajax/team/(?P<team_id>\d+)/member/remove/(?P<userprofile_id>\d+)/', remove_team_member, name='remove_team_member'),
    url(r'ajax/team/(?P<team_id>\d+)/owner/create/(?P<userprofile_id>\d+)/', make_team_owner, name='make_team_owner'),
    url(r'ajax/team/owner/remove/(?P<share_tree_id>\d+)/', undo_team_owner, name='undo_team_owner'),

    url(r'team/add/$', add_team, name='add_team'),
    url(r'team/(?P<team_id>\d+)/edit/$', EditTeamView.as_view(), name='edit_team'),
    url(r'team/(?P<team_id>\d+)/delete/', delete_team, name='delete_team'),
    url(r'team/(?P<team_id>\d+)/', view_team, name='view_team'),

    url(r'settings/$', view_settings, name='settings'),
    url(r'settings/update/places/$', view_settings, {'update_places': True}, name='update_places'),
    url(r'settings/update/user/$', view_settings, {'update_user': True}, name='edit_private_info'),


    url(r'$', view_contacts, name='view_contacts'),
)

