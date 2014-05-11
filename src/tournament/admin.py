from django.contrib import admin

from tournament.models import Tag, PlayField, Competition, Tournament, Participation

admin.site.register(Tag)
admin.site.register(PlayField)
admin.site.register(Competition)
admin.site.register(Tournament)
admin.site.register(Participation)

