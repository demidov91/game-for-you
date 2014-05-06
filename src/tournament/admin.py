from django.contrib import admin

from tournament.models import Tag, PlayField, Competition, Tournament

admin.site.register(Tag)
admin.site.register(PlayField)
admin.site.register(Competition)
admin.site.register(Tournament)

