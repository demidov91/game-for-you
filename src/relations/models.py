import os
import uuid

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.core.urlresolvers import reverse

from allauth.socialaccount.signals import pre_social_login

from core.models import ShareTree
from chat.models import Chat

import logging
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """
    Contacts describe only this instance, so you can create contacts which describe unregistered users.
    """
    DEFAULT_USER_PICK = os.path.join(settings.MEDIA_URL, 'upload', 'user_picks', 'owl.jpg')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    #Some greeting text to be displayed next to profile.
    status = models.TextField(blank=True)
    #Team to display on authenticated_index page.
    primary_team = models.ForeignKey('relations.Team', null=True, blank=True, on_delete=models.SET_NULL)
    patronymic = models.CharField(max_length=100, default='', blank=True, verbose_name=_('patronymic'))
    image = models.ImageField(upload_to='upload/user_picks',
                              default=DEFAULT_USER_PICK,
                              max_length=255, verbose_name=_('userpick'), blank=True, null=False)
    external_image = models.URLField(verbose_name=_('external userpick'),
                                     help_text=_('Save server space - use external images.'
                                                 ' Leave this field blank to use uploaded userpick.'),
                                     null=True, blank=True,)
    external_read_auth = models.CharField(max_length=100, default=None, null=True, blank=False, unique=True,
                                          verbose_name=_('Authenticate by get parameter parameter'))

    def get_full_name(self):
        """
        Full name or username.
        """
        if self.user:
            if self.user.last_name or self.user.first_name or self.patronymic:
                return u'{0} {1} {2}'.format(self.user.last_name, self.user.first_name, self.patronymic)
            else:
                return self.user.username
        return 'No user.'

    def get_short_name(self):
        if self.user:
            return self.user.get_short_name() or self.user.username
        return 'No user. (Short name)'

    def __str__(self):
        return self.get_full_name()

    def get_active_teams(self):
        """
        returns: Collection of *Team* objects.
        """
        return self.teams.filter(is_draft=False)

    def get_image(self):
        return self.external_image or self.image.url

    def get_primary_team(self):
        """
        returns: *primary_team* or just first team from the *active_teams* list.
        """
        if not self.primary_team:
            self.primary_team = self.get_active_teams().first()
            self.save()
        return self.primary_team


@receiver(pre_social_login)
def handler(sender, sociallogin, **kwargs):
    UserProfile.objects.filter(user=sociallogin.account.user).update(external_image=sociallogin.account.get_avatar_url())


@receiver(post_save, sender=User)
def _create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, external_read_auth=uuid.uuid1().hex)



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


@python_2_unicode_compatible
class Team(models.Model):
    DEFAULT_NAME = _('NoName (c)')

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(UserProfile, related_name='teams')
    owner = models.ForeignKey(ShareTree)
    is_draft = models.BooleanField(default=True)
    chat = models.ForeignKey(Chat, null=False, blank=False)

    def __str__(self):
        return self.get_name_or_default()

    def get_name_or_default(self):
        return force_text(self.name or Team.DEFAULT_NAME)

    def get_absolute_url(self):
        return reverse('view_team', args=(self.id, ))


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
