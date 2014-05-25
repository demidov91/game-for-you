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


def get_calendar_events_by_tags(tags, start, end, owner=None):
    tournaments = Tournament.objects.filter(tags__in=tags, last_datetime__gte=start, first_datetime__lte=end).distinct()
    competitions = Competition.objects.filter(tags__in=tags, start_datetime__range=(start, end)).distinct()
    events = []
    if owner and owner.is_authenticated():
        tournaments_of_interest = Tournament.objects.filter(
            Q(owners__shared_to__in=(owner,)) & Q(last_datetime__gte=start) & Q(first_datetime__lte=end) &
            (Q(tags=None) & Q(tags_request=None) | ~Q(tags_request=None))).distinct()
        danger_tournaments = tournaments_of_interest.filter(tags=None)
        warn_tournaments = tournaments_of_interest.exclude(tags=None)
        competitions_of_interest = Competition.objects.filter(
            Q(owners__shared_to__in=(owner,)) &
            Q(start_datetime__range=(start, end)) &
            (Q(tags=None) & Q(tags_request=None) | ~Q(tags_request=None))).distinct()
        danger_competitions = competitions_of_interest.filter(tags=None)
        warn_competitions = competitions_of_interest.exclude(tags=None)
        tournaments = tournaments.exclude(id__in=tournaments_of_interest.values_list('id', flat=True))
        competitions = competitions.exclude(id__in=competitions_of_interest.values_list('id', flat=True))
        events += tournaments_to_calendar_events(danger_tournaments, class_name='no-tags')
        events += tournaments_to_calendar_events(warn_tournaments, class_name='has-tags-to-approve')
        events += competitions_to_calendar_events(danger_competitions, class_name='no-tags')
        events += competitions_to_calendar_events(warn_competitions, class_name='has-tags-to-approve')
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
        'competitions':  Competition.objects.filter(tags__in=tags,
                                                    start_datetime__gte=day,
                                                    start_datetime__lt=next_day),
    }

def tournaments_to_calendar_events(tournaments, class_name=''):
    return tuple({
        'title': t.name,
        'start': to_timestamp(t.first_datetime),
        'end': to_timestamp(t.last_datetime),
        'url': reverse('view_tournament', kwargs={'tournament_id': t.id, }),
        'className': 'tournament ' + class_name,
    } for t in tournaments)

def competitions_to_calendar_events(competitions, class_name=''):
    return tuple({
        'title': c.get_name(),
        'start': to_timestamp(c.start_datetime),
        'url': reverse('view_competition', kwargs={'competition_id': c.id}),
        'className': 'competition ' + class_name,
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


class BaseManagementTreeUtil(ShareTreeUtil):
    def is_manager(self, managed, user):
        return managed.owners.filter(shared_to=user).exists()

class TagOwnersTreeUtil(BaseManagementTreeUtil):
    model_class = TagManagementTree
    def _is_tree_member(self, leaf):
        return leaf and self.model_class.objects.get(id=leaf.id).permissions == TagManagementTree.OWNER

class TagPublishersTreeUtil(BaseManagementTreeUtil):
    def is_manager(self, managed, user):
        return managed.sharers.filter(shared_to=user).exists()

_base_owners_util = BaseManagementTreeUtil()

def is_owner(managed, user):
    return _base_owners_util.is_manager(managed, user)


def create_tags(names, owner):
    """
    names: *str* iterable.
    owner: *auth.User* instance.
    returns: *int* iterable.
    """
    new_tag_ids = []
    for name in names:
        tag = Tag.objects.create(name=name)
        TagManagementTree.objects.create(managed=tag, shared_to=owner, permissions=TagManagementTree.OWNER)
        new_tag_ids.append(tag.id)
    return new_tag_ids