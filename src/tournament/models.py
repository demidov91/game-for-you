from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.conf import settings

from relations.models import Team, Contact
from core.models import ShareTree

import logging
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Tag(models.Model):
    """
    Event topic.
    """
    #People who view events
    subscribers = models.ManyToManyField(get_user_model(), related_name='subscribed_to', null=True, blank=True)
    #Displayed name.
    name = models.CharField(max_length=100, verbose_name=_('name'), unique=True)
    #Tag chat enabled.
    has_chat = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def sharers(self):
        return self.managers.filter(permissions=TagManagementTree.PUBLISHER)

    @property
    def owners(self):
        return self.managers.filter(permissions=TagManagementTree.OWNER)


@python_2_unicode_compatible
class TagManagementTree(ShareTree):
    #Publisher can add publishers and remove publishers from 'his' sharing tree.
    #Public their and proposed events with managed tag.
    PUBLISHER = 0
    #Owner has as much rights as sharer, can add and remove sharers, remove owners from 'his' ownership tree.
    #Last owner can delete a tag.
    OWNER = 1

    managed = models.ForeignKey(Tag, related_name='managers')
    permissions = models.PositiveSmallIntegerField(default=PUBLISHER, null=False, blank=False)

    def __str__(self):
        return u'{0} {1} {2}'.format(super(TagManagementTree, self).__str__(), _('for tag'), str(self.managed))

@receiver(post_save, sender=get_user_model())
def add_default_tag(sender, instance, created, **kwargs):
    if created:
        instance.subscribed_to.add(*Tag.objects.filter(id__in=settings.DEFAULT_TAGS))

@python_2_unicode_compatible
class Tournament(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    first_datetime = models.DateTimeField(verbose_name=_('first date'))
    last_datetime = models.DateTimeField(verbose_name=_('last date'))
    tags = models.ManyToManyField(Tag, related_name='tournaments', verbose_name=_('tags'), null=True, blank=True)
    tags_request = models.ManyToManyField(Tag, related_name='tournament_requests')

    def __str__(self):
        return self.name or _('No-name tournament')


@python_2_unicode_compatible
class PlayField(models.Model):
    """
    Place where game can be held.
    """
    name = models.CharField(max_length=100, verbose_name=_('place name'), null=True, blank=True, default='')
    address = models.TextField(verbose_name=_('address'), null=True, blank=True, default='')
    owner = models.ForeignKey(get_user_model(), verbose_name=_('owner'), related_name='known_places')

    def __str__(self):
        return self.get_short_description()

    def get_short_description(self):
        """
        returns: *str*. Place name or address.
        """
        return self.name or self.address

@python_2_unicode_compatible
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

    tournament = models.ForeignKey(Tournament,
                                   verbose_name=_('tournament'),
                                   null=True,
                                   blank=True,
                                   related_name='competitions',
                                   on_delete=models.SET_NULL)
    place = models.ForeignKey(PlayField, verbose_name=_('place to play'), on_delete=models.PROTECT)
    start_datetime = models.DateTimeField(verbose_name=_('start date'))
    #duration in minutes
    duration = models.IntegerField(null=True, blank=True, verbose_name=_('competition duration (in minutes)'))
    team_limit = models.IntegerField(null=True, blank=True, verbose_name=_('max team count'))
    team_accept_strategy = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, verbose_name=_('team accept strategy'))
    tags = models.ManyToManyField(Tag, related_name='competitions', verbose_name=_('tags'), null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=_('competition name'), null=True, blank=True)
    tags_request = models.ManyToManyField(Tag, related_name='competition_requests')

    def get_name(self):
        return force_text(self.name or self.tournament and self.tournament.name or _('No-name competition'))

    def __str__(self):
        return u'{0} {1} {2}'.format(self.get_name(), _('in'), self.place.get_short_description())


@python_2_unicode_compatible
class TournamentOwnersTree(ShareTree):
    managed = models.ForeignKey(Tournament, related_name='owners')


@python_2_unicode_compatible
class CompetitionOwnersTree(ShareTree):
    managed = models.ForeignKey(Competition, related_name='owners')


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

    team = models.ForeignKey(Team, related_name='participations')
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




