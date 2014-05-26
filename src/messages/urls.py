from django.conf.urls import patterns,  url

from messages.views import *


urlpatterns = patterns('',
    url(r'^ajax/tag/(?P<tag_id>\d+)/$', tag_chat, name='tag_chat'),
)
