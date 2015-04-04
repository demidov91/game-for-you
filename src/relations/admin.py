from django.contrib import admin

from relations.models import UserProfile, Team


class TeamAdmin(admin.ModelAdmin):
    fields = ('name', 'members')


admin.site.register(UserProfile)
admin.site.register(Team, TeamAdmin)

