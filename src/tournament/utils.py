from datetime import timedelta

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.conf import settings

from tournament.models import Tag, Tournament, Competition, Participation, TagManagementTree
from core.utils import to_timestamp, ShareTreeUtil

import logging
logger = logging.getLogger(__name__)


class TagsProvider:
    def __init__(self, request):
        pass

    def _get_tag_by_name(self, name):
        return Tag.objects.get(name=name)

    def get_tags(self):
        """
        returns: *iterable* of *Tag* instances.
        """
        raise NotImplementedError()

    def remove_tag_by_id(self, id):
        """
        Unsubscribe or fail silently.
        """
        raise NotImplementedError()

    def add_tag_by_name(self, name):
        """
        Subscribe.
        name: *Tag.name* value.
        raises: *Tag.DoesNotExist*.
        """
        raise NotImplementedError()


class AuthenticatedTagsProvider(TagsProvider):
    def __init__(self, request):
        self.user = request.user

    def get_tags(self):
        return self.user.subscribed_to.all()

    def remove_tag_by_id(self, id):
        self.user.subscribed_to.remove(id)

    def add_tag_by_name(self, name):
        self.user.subscribed_to.add(self._get_tag_by_name(name))


class NoneAuthenticatedTagsProvider(TagsProvider):
    request = None
    session = None
    SESSION_KEY = 'tags'

    def __init__(self, request):
        self.session = request.session

    def _get_tags_id(self):
        """
        returns: iterable of *int*.
        """
        ids = self.session.get(self.SESSION_KEY)
        if ids is None:
            ids = get_default_tag_ids(self.request)
        return ids

    def get_tags(self):
        return Tag.objects.filter(id__in=self._get_tags_id())

    def remove_tag_by_id(self, id):
        ids = list(self._get_tags_id())
        if id in ids:
            ids.remove(id)
            self.session[self.SESSION_KEY] = ids

    def add_tag_by_name(self, name):
        ids = list(self._get_tags_id())
        ids.append(self._get_tag_by_name(name).id)
        self.session[self.SESSION_KEY] = ids



def get_default_tag_ids(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators
    returns: **tuple** of **int**.
    """
    return settings.DEFAULT_TAGS

def get_tags_provider(request):
    """
    returns: *TagsProvider* instance.
    """
    return (AuthenticatedTagsProvider if request.user.is_authenticated() else NoneAuthenticatedTagsProvider)(request)


def get_calendar_events_by_tags(tags, start, end):
    tournaments = Tournament.objects.filter(tags__in=tags, last_datetime__gte=start, first_datetime__lte=end).distinct()
    competitions = Competition.objects.filter(tags__in=tags, start_datetime__range=(start, end)).distinct()
    events = []
    events += tournaments_to_calendar_events(tournaments)
    events += competitions_to_calendar_events(competitions)
    return events

def get_calendar_events_by_team(team, start, end):
    competitions_id = team.participations.filter(Q(state=Participation.CLAIM) | Q(state=Participation.APPROVED)).values_list('competition_id', flat=True)
    competitions = Competition.objects.filter(id__in=competitions_id, start_datetime__range=(start, end))
    events = competitions_to_calendar_events(competitions)
    return events


def get_events_by_tags_and_day(tags, day):
    next_day = day + timedelta(days=1)
    return {
        'tournaments': Tournament.objects.filter(tags__in=tags, first_datetime__lte=day, last_datetime__gte=day),
        'competitions':  Competition.objects.filter(tags=tags,
                                                    start_datetime__gte=day,
                                                    start_datetime__lt=next_day),
    }

def tournaments_to_calendar_events(tournaments):
    return tuple({
        'title': t.name,
        'start': to_timestamp(t.first_datetime),
        'end': to_timestamp(t.last_datetime),
        'url': reverse('view_tournament', kwargs={'tournament_id': t.id, })
    } for t in tournaments)

def competitions_to_calendar_events(competitions):
    return tuple({
        'title': c.get_name(),
        'start': to_timestamp(c.start_datetime),
        'url': reverse('view_competition', kwargs={'competition_id': c.id}),
    } for c in competitions)


def get_default_participation_state(competition):
    """
    Returns value for *Team.state* by *Competition.team_accept_strategy*.
    **competition**: *Competition* instance.
    """
    if competition.team_accept_strategy == Competition.OPEN_STRATEGY:
        return Participation.APPROVED
    if competition.team_accept_strategy == Competition.PRIVATE_STRATEGY:
        return Participation.CLAIM
    return Participation.CLAIM

class TagOwnersTreeUtil(ShareTreeUtil):
    def _is_tree_member(self, leaf):
        return leaf and leaf.permissions == TagManagementTree.OWNER