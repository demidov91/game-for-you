from django.conf.urls import patterns,  url

from tournament.views import *
from tournament.utils import OpenChatFeed


urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^ajax/calendar-events/one-day/$', calendar_events_for_day_ajax, name='get_calendar_events_for_day'),
    url(r'^ajax/calendar-events/$', calendar_events_json, name='get_calendar_events'),
    url(r'^ajax/calendar-events/team/(?P<team_id>\d+)/$', calendar_events_for_team_json, name='get_calendar_events_for_team'),
    url(r'^ajax/competition/(?P<competition_id>\d+)/add/team/', add_participation_request, name='add_participation_request'),
    url(r'^ajax/competition/(?P<participation_id>\d+)/remove/team/', undo_participation_request, name='undo_participation_request'),
    url(r'^ajax/participation/(?P<participation_id>\d+)/state/(?P<state>\d)/', manage_participation_request, name='change_participation'),
    url(r'^ajax/competition/(?P<competition_id>\d+)/$', view_competition_part, name='view_competition_part'),
    url(r'^ajax/tag/list/', get_tag_names, name='get_tag_names'),
    url(r'^ajax/tag/(?P<tag_id>\d+)/owners/list/', get_tag_managers_list, name='tag_managers_list'),
    url(r'^ajax/tag/(?P<tag_id>\d+)/publishers/list/', get_tag_publishers_list, name='tag_publishers_list'),
    url(r'^ajax/tag/add/owner/(?P<manager_id>\d+)/', make_tag_owner, name='make_tag_owner'),
    url(r'^ajax/tag/(?P<tag_id>\d+)/sharer/add/(?P<user_id>\d+)/', add_tag_sharer, name='make_tag_sharer'),
    url(r'^ajax/tag/(?P<manager_id>\d+)/owner/remove/', downgrade_to_tag_sharer, name='remove_tag_owner'),
    url(r'^ajax/tag/(?P<manager_id>\d+)/sharer/remove/', remove_tag_sharer, name='remove_tag_sharer'),
    url(r'^ajax/(?P<model_key>tournament|competition|tag)/(?P<owner_id>\d+)/chat/$', authenticated_chat, name='authenticated_chat'),

    url(r'^event/add/$', add_event, name='add_event'),
    url(r'^tournament/add/$', add_tournament, name='add_tournament'),
    url(r'^competition/add/$', add_competition, name='add_competition'),
    url(r'^competition/(?P<competition_id>\d+)/$', view_competition, name='view_competition'),
    url(r'^competition/(?P<competition_id>\d+)/edit/$', edit_competition, name='edit_competition'),
    url(r'^tournament/(?P<tournament_id>\d+)/$', view_tournament, name='view_tournament'),
    url(r'^tournament/(?P<tournament_id>\d+)/edit/$', edit_tournament, name='edit_tournament'),
    url(r'^tournament/(?P<tournament_id>\d+)/delete/$', delete_tournament, name='delete_tournament'),
    url(r'^competition/(?P<competition_id>\d+)/delete/$', delete_competition, name='delete_competition'),
    url(r'^tag/unsubscribe/$', change_tag_subscription_state, {'subscribe': False}, name='unsubscribe_tag'),
    url(r'^tag/subscribe/$', change_tag_subscription_state, {'subscribe': True}, name='subscribe_tag'),
    url(r'^tag/(?P<tag_id>\d+)/edit/$', edit_tag, name='edit_tag'),
    url(r'^tag/(?P<tag_id>\d+)/delete/$', delete_tag, name='delete_tag'),
    url(r'^tag/(?P<tag_id>\d+)/accept/competition/(?P<event_id>\d+)/$', accept_tag_request,
        {'event_model_class': Competition}, name='accept_competition_tag'),
    url(r'^tag/(?P<tag_id>\d+)/accept/tournament/(?P<event_id>\d+)/$', accept_tag_request,
        {'event_model_class': Tournament}, name='accept_tournament_tag'),
    url(r'^tag/(?P<tag_id>\d+)/$', tag_page, name='tag_page'),
    url(r'^tag/create/$', create_tag, name='tag_create'),

    url(r'^rss/chat/(?P<model_key>tournament|competition|tag)/(?P<id>\d+)/', OpenChatFeed(), name='open_rss'),
    url(r'^chat/open/(?P<model_key>tournament|competition|tag)/message/(?P<id>\d+)/', redirect_to_message_in_authenticated_chat, name='open_chat_message'),
)

