from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models

from relations.models import Team, Contact

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    first_datetime = models.DateTimeField()
    last_datetime = models.DateTimeField()


class PlayField(models.Model):
    """
    Place where game can be held.
    """
    name = models.CharField(max_length=100)
    address = models.TextField()


class Competition(models.Model):
    """
    Bag for *Tournament* and *PlayField*
    """
    OPEN_STRATEGY = 0
    PRIVATE_STRATEGY = 1

    STRATEGY_CHOICES = (
        (OPEN_STRATEGY, _('open')),
        (PRIVATE_STRATEGY, _('private')),
    )

    tournament = models.ForeignKey(Tournament)
    place = models.ForeignKey(PlayField)
    start_datetime = models.DateTimeField()
    #duration in minutes
    duration = models.IntegerField(null=True)
    team_limit = models.IntegerField(null=True)
    team_accept_strategy = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES)


class Participation(models.Model):
    """
    Bag for *Competition* and *Team*.
    """
    INVITATION = 0
    CLAIM = 1
    APPROVED = 2
    DECLINED = 3
    REGISTERED = 4

    STATE_CHOICES = (
        (INVITATION, _('invitation')),
        (CLAIM, _('claim')),
        (APPROVED, _('approved')),
        (DECLINED, _('declined')),
        (REGISTERED, _('registered')),
    )

    team = models.ForeignKey(Team)
    competition = models.ForeignKey(Competition)
    creator = models.ForeignKey(get_user_model())
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    greeting_words = models.TextField()
    answer = models.TextField()


class PlayerParticipation(Contact):
    """
    Users that play in team during one game.
    """
    participation = models.ForeignKey(Participation)


class Tag(models.Model):
    """
    Event topic.
    """
    #Owner has as much rights as sharer, can add and remove sharers, remove owners from 'his' ownership tree.
    # Last owner can delete a tag.
    first_owners = models.ManyToManyField(get_user_model(), related_name='tags_owned')
    #Sharer can add sharers and remove sharers from 'his' sharing tree. Public their and proposed events with this tag.
    first_sharers = models.ManyToManyField(get_user_model(), related_name='tags_to_publish')
    #People who are viewing events
    subscribers = models.ManyToManyField(get_user_model(), related_name='subscribed_to', null=True, blank=True)
    #Displayed name.
    name = models.CharField(max_length=100)


