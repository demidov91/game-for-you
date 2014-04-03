from django.conf.urls import patterns, include, url

from django.contrib import admin
from tournament import urls as tournament_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'game_for_everyone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(tournament_urls)),
)
