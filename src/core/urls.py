from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import django
from django.conf.urls.static import static
from django.contrib.flatpages.views import flatpage

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
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^ru/about/', flatpage, {'url': '/ru/about/'}, name='about_ru'),
    url(r'^by/about/', flatpage, {'url': '/by/about/'}, name='about_by'),
    url(r'', include(tournament_urls)),
)

if settings.DEBUG and django.VERSION < (1, 6):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
