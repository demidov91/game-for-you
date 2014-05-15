from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from core.models import ShareTree


class UserProfile(models.Model):
    """
    Contacts describe only this instance, so you can create contacts which describe unregistered users.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    #Some greeting text to be displayed next to profile.
    status = models.TextField(blank=True)
    #Team to display on authenticated_index page.
    primary_team = models.ForeignKey('relations.Team', null=True, blank=True, on_delete=models.SET_NULL)

    patronymic = models.CharField(max_length=100, default='', blank=True)

    def get_full_name(self):
        """
        Full name or username.
        """
        if self.user:
            return (self.user.last_name + self.user.first_name + (self.patronymic or '')) or self.user.username
        return 'No user.'

    def get_short_name(self):
        if self.user:
            return self.user.get_short_name() or self.user.username
        return 'No user. (Short name)'

    def __unicode__(self):
        return self.get_full_name()

    def get_active_teams(self):
        """
        returns: Collection of *Team* objects.
        """
        return self.teams.filter(is_draft=False)

    def get_image(self):
        return settings.STATIC_URL + 'img/owl.jpg'


@receiver(post_save, sender=User)
def _create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserProfileRecordType(models.Model):
    """
    Principal record type. It's name can be localized.
    """
    system_name = models.CharField(max_length=100)


class UserProfileRecordTypeName(models.Model):
    """
    Localizations for record types.
    """
    type = models.ForeignKey(UserProfileRecordType)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=5)


class UserProfileRecord(models.Model):
    type = models.ForeignKey(UserProfileRecordType)
    value = models.TextField()
    order = models.IntegerField()


class Team(models.Model):
    DEFAULT_NAME = _('NoName (c)')

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(UserProfile, related_name='teams')
    owner = models.ForeignKey(ShareTree)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return str(self.get_name_or_default())

    def get_name_or_default(self):
        return self.name or Team.DEFAULT_NAME


class Contact(models.Model):
    """
    Contact which is connected to user. Owner is not defined yet.
    """
    about = models.ForeignKey(UserProfile)


class UserContact(Contact):
    """
    Contact between 2 users.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='known_people')


class TeamContact(Contact):
    """
    Contact between team and user.
    """
    owner = models.ForeignKey(Team)


class KnownTeam(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    about = models.ForeignKey(Team)


class ContactRecord(UserProfileRecord):
    contact = models.ForeignKey(Contact)
    is_encrypted = models.BooleanField(default=False)


class OwnRecord(UserProfileRecord):
    IS_PUBLIC = 0
    FOR_TEAM = 1
    IS_PRIVATE = 2

    SHARED_BETWEEN_CHOICES = (
        (IS_PUBLIC, _('Is public record')),
        (FOR_TEAM, _('Record for team')),
        (IS_PRIVATE, _('Is private record')),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='own_records', null=True)
    shared_between = models.PositiveSmallIntegerField(choices=SHARED_BETWEEN_CHOICES)
