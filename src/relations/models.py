from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django.db import models


class UserProfile(models.Model):
    """
    Contacts describe only this instance, so you can create contacts which describe unregistered users.
    """
    user = models.OneToOneField(get_user_model(), null=True)
    #Some greeting text to be displayed next to profile.
    status = models.TextField()


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
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(UserProfile)


class Contact(models.Model):
    """
    Contact which is connected to user. Owner is not defined yet.
    """
    about = models.ForeignKey(UserProfile)


class UserContact(Contact):
    """
    Contact between 2 users.
    """
    owner = models.ForeignKey(get_user_model())


class TeamContact(Contact):
    """
    Contact between team and user.
    """
    owner = models.ForeignKey(Team)


class KnownTeam(models.Model):
    owner = models.ForeignKey(get_user_model())
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

    owner = models.ForeignKey(get_user_model(), null=True)
    shared_between = models.PositiveSmallIntegerField(choices=SHARED_BETWEEN_CHOICES)
