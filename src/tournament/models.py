from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model
from django.db import models

from relations.models import Team, Contact
from core.models import ShareTree


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
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    first_datetime = models.DateTimeField()
    last_datetime = models.DateTimeField()
    tags = models.ManyToManyField(Tag, related_name='tournaments')


class PlayField(models.Model):
    """
    Place where game can be held.
    """
    name = models.CharField(max_length=100, verbose_name=_('place name'))
    address = models.TextField(verbose_name=_('address'))
    owner = models.ForeignKey(get_user_model(), verbose_name=_('owner'))
    sharers = models.ManyToManyField(get_user_model(), verbose_name=_('people who know this place'), related_name='known_places')

    def __str__(self):
        return self.name


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

    tournament = models.ForeignKey(Tournament, verbose_name=_('tournament'), null=True, blank=True)
    place = models.ForeignKey(PlayField, verbose_name=_('place to play'))
    start_datetime = models.DateTimeField(verbose_name=_('start date'))
    #duration in minutes
    duration = models.IntegerField(null=True, blank=True, verbose_name=_('competition duration (in minutes)'))
    team_limit = models.IntegerField(null=True, blank=True, verbose_name=_('max team count'))
    team_accept_strategy = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, verbose_name=_('team accept strategy'))
    tags = models.ManyToManyField(Tag, related_name='competitions', verbose_name=_('tags'))
    name = models.CharField(max_length=100, verbose_name=_('competition name'), null=True, blank=True)
    owners = models.ForeignKey(ShareTree)

    def get_name(self):
        return self.tournament.name if self.tournament else self.name or ''

    def __str__(self):
        return '{0} {1} {2}'.format(self.get_name(), _('in'), self.place.name)


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




