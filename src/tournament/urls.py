from django.conf.urls import patterns, include, url

from tournament.views import *

urlpatterns = patterns('',
    url(r'$', index, name='all_events_calendar_page'),

    url(r'ajax/calendar-events/$', calendar_events_json, name='get_calendar_events')
)

