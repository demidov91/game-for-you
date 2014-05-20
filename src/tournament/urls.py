from django.conf.urls import patterns, include, url

from tournament.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^ajax/calendar-events/one-day/$', calendar_events_for_day_ajax, name='get_calendar_events_for_day'),
    url(r'^ajax/calendar-events/$', calendar_events_json, name='get_calendar_events'),
    url(r'^ajax/calendar-events/team/(?P<team_id>\d+)/$', calendar_events_for_team_json, name='get_calendar_events_for_team'),
    url(r'^ajax/competition/(?P<competition_id>\d+)/add/team/', add_participation_request, name='add_participation_request'),
    url(r'^ajax/competition/(?P<participation_id>\d+)/remove/team/', undo_participation_request, name='undo_participation_request'),
    url(r'^ajax/participation/(?P<participation_id>\d+)/state/(?P<state>\d)/', manage_participation_request, name='change_participation'),
    url(r'^ajax/competition/(?P<competition_id>\d+)/', view_competition_part, name='view_competition_part'),
    url(r'^ajax/tag/(?P<tag_id>\d+)/unsubscribe/', unsubscribe_tag, name='unsubscribe_tag'),

    url(r'^event/add/$', add_event, name='add_event'),
    url(r'^tournament/add/$', add_tournament, name='add_tournament'),
    url(r'^competition/add/$', add_competition, name='add_competition'),
    url(r'^competition/(?P<competition_id>\d+)/$', view_competition, name='view_competition'),
    url(r'^tournament/(?P<tournament_id>\d+)/$', view_tournament, name='view_tournament'),
    url(r'^tournament/(?P<tournament_id>\d+)/delete/$', delete_tournament, name='delete_tournament'),
    url(r'^competition/(?P<competition_id>\d+)/delete/$', delete_competition, name='delete_competition'),
    url(r'^tag/(?P<tag_id>\d+)/$', tag_page, name='tag_page'),
)

