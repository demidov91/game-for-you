from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static

from tournament import urls as tournament_urls
from relations import urls as relations_urls
from allauth.account.views import logout


admin.autodiscover()

urlpatterns = patterns('',
    url(r'admin/logout/', logout, name='protected_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'contacts/', include(relations_urls)),
    url(r'', include(tournament_urls)),
)

if settings.SERVE_STATIC:
    urlpatterns += (
        url(r'^{0}(?P<path>.*)$'.format(settings.STATIC_URL[1:len(settings.STATIC_URL)]), serve_static),
    )
