from django.contrib import admin

from tournament.models import Tag, PlayField, Competition, Tournament, Participation, TagManagementTree,\
    TournamentOwnersTree, CompetitionOwnersTree

admin.site.register(Tag)
admin.site.register(PlayField)
admin.site.register(Competition)
admin.site.register(Tournament)
admin.site.register(Participation)
admin.site.register(TagManagementTree)
admin.site.register(TournamentOwnersTree)
admin.site.register(CompetitionOwnersTree)

