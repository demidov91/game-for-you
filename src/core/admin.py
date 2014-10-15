from django.contrib import admin
from django.contrib.flatpages.admin import FlatPage, FlatPageAdmin, FlatpageForm
from django import forms
from django.conf import settings
from ckeditor.widgets import CKEditorWidget

from core.models import ShareTree


class FlatPageFormReachText(FlatpageForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='event'))

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdminReachText(FlatPageAdmin):
    form = FlatPageFormReachText

    class Media:
        js = (settings.STATIC_URL + 'js/lib/jquery-2.0.2.min.js',
              settings.STATIC_URL + 'ckeditor/ckeditor/ckeditor.js',
              settings.STATIC_URL + 'ckeditor/ckeditor-init.js',)


admin.site.register(ShareTree)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminReachText)