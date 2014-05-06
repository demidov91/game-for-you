from django.conf.urls import patterns, include, url

from tournament.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^ajax/calendar-events/one-day/$', calendar_events_for_day_ajax, name='get_calendar_events_for_day'),
    url(r'^ajax/calendar-events/$', calendar_events_json, name='get_calendar_events'),
    url(r'^ajax/competition/(?P<competition_id>\d+)/add/team/', add_participation_request, name='add_participation_request'),
    url(r'^ajax/competition/(?P<participation_id>\d+)/remove/team/', undo_participation_request, name='undo_participation_request'),
    url(r'^ajax/competition/(?P<participation_id>\d+)/accept/team/', accept_participation_request, name='accept_participation_request'),
    url(r'^event/add/$', add_event, name='add_event'),
    url(r'^tournament/add/$', add_tournament, name='add_tournament'),
    url(r'^competition/add/$', add_competition, name='add_competition'),
    url(r'^competition/(?P<competition_id>\d+)/$', view_competition, name='view_competition'),
)

