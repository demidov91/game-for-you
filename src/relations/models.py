from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django.db import models


class UserProfile(models.Model):
    """
    Contacts describe only this instance, so you can create contacts which describe unregistered users.
    """
    user = models.OneToOneField(get_user_model(), null=True)


class Team(models.Model):
    name = models.CharField(max_length=255)


class Contact(models.Model):
    """
    Contact either between 2 users or between team and user (team know user).
    """
    owner = models.ForeignKey(get_user_model())
    about = models.ForeignKey(UserProfile)


class TeamContact(models.Model):
    """
    Contact between team and user.
    """
    owner = models.ForeignKey(Team)
    is_member = models.BooleanField(default=False)



class SingleContactRecord(models.Model):
    """
    Record of variable type. Record is stored as string, 'view' should render it according to the *type*.
    """
    TEXT_TYPE = 1
    PHONE_NUMBER_TYPE = 2

    IS_PUBLIC = 0
    FOR_TEAM = 1
    IS_PRIVATE = 2

    DATA_FIELD_CHOICES = (
        (TEXT_TYPE, _('Text type')),
        (PHONE_NUMBER_TYPE, _('Phone number type')),
    )

    SHARED_BETWEEN_CHOICES = (
        (IS_PUBLIC, _('Is public record')),
        (FOR_TEAM, _('Record for team')),
        (IS_PRIVATE, _('Is private record')),
    )

    unique_together = ('contact', 'team_contact', 'sharer')
    user_contact = models.ForeignKey(Contact, null=True)
    team_contact = models.ForeignKey(TeamContact, null=True)
    sharer = models.ForeignKey(get_user_model(), null=True)
    name = models.CharField(max_length=255)
    value = models.TextField()
    type = models.PositiveSmallIntegerField(choices=DATA_FIELD_CHOICES)
    shared_between = models.PositiveSmallIntegerField(choices=SHARED_BETWEEN_CHOICES)

