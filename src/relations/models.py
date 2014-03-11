from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django.db import models

from core.models import PropertyRecord


class UserProfile(models.Model):
    """
    Contacts describe only this instance, so you can create contacts which describe unregistered users.
    """
    user = models.OneToOneField(get_user_model(), null=True)


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField()


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


class ContactRecord(PropertyRecord):
    contact = models.ForeignKey(Contact)
    is_encrypted = models.BooleanField(default=False)


class OwnRecord(PropertyRecord):
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
