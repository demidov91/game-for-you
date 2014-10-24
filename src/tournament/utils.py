from datetime import timedelta
import sys

from django.db.models import Q, Count
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404

from tournament.models import Tag, Tournament, Competition, Participation, TagManagementTree
from core.utils import to_timestamp, ShareTreeUtil
from chat.utils import ChatFeed
from chat.models import Message

import logging
logger = logging.getLogger(__name__)


# *dict* to convert chat provider url key into model class.
KEY_TO_CHAT_OWNER = {
    'tag': Tag,
    'tournament': Tournament,
    'competition': Competition,
}

# reverse for **KEY_TO_CHAT_OWNER**
CHAT_OWNER_TO_URL_KEY = { }

for key, value in KEY_TO_CHAT_OWNER.items():
    CHAT_OWNER_TO_URL_KEY[value] = key


class TagsProvider:
    FIRST_POPULAR_TAGS = 10

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

    def add_tag_by_id(self, id):
        """
        Subscribe.
        id: *Tag.id* value.
        raises: *Tag.DoesNotExist*.
        """
        raise NotImplementedError()

    def show_draft(self):
        return True

    def get_other_tags(self):
        """
        returns: pair of 2 lists. 1st list is for popular tags, 2nd list is for all other tags.
        """
        all_other_tags = Tag.objects.filter(is_private=False).exclude(id__in=self.get_tags().\
            values_list('id', flat=True)).annotate(subscribers_count=Count('subscribers')).order_by('subscribers_count')
        return all_other_tags[:self.FIRST_POPULAR_TAGS], all_other_tags[self.FIRST_POPULAR_TAGS:]



class AuthenticatedTagsProvider(TagsProvider):
    def __init__(self, request):
        self.user = request.user

    def get_tags(self):
        return self.user.subscribed_to.all()

    def remove_tag_by_id(self, id):
        self.user.subscribed_to.remove(id)

    def add_tag_by_name(self, name):
        self.user.subscribed_to.add(self._get_tag_by_name(name))

    def add_tag_by_id(self, id):
        self.user.subscribed_to.add(Tag.objects.get(id=id))



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

    def add_tag_by_id(self, id):
        ids = list(self._get_tags_id())
        ids.append(id)
        self.session[self.SESSION_KEY] = ids

class LimitedTagsProvider(TagsProvider):
    REQUEST_KEY = 'tag_only'
    def __init__(self, request):
        self.tag = Tag.objects.filter(id=int(request.GET[self.REQUEST_KEY]))
    def get_tags(self):
        return self.tag
    def show_draft(self):
        return False


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
    if request.method == 'GET' and request.GET.get(LimitedTagsProvider.REQUEST_KEY):
        return LimitedTagsProvider(request)
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


def get_events_by_tags_and_day(tags, day, owner=None):
    next_day = day + timedelta(days=1)
    event_additional_query = Q(tags__in=tags)
    if owner and owner.is_authenticated():
        problem_event_query = \
            Q(owners__shared_to__in=(owner,)) & (Q(tags=None) & Q(tags_request=None) | ~Q(tags_request=None))
        event_additional_query = event_additional_query | problem_event_query
    return {
        'tournaments': Tournament.objects.filter(
            Q(first_datetime__lte=day) &
            Q(last_datetime__gte=day)
            & event_additional_query),
        'competitions':  Competition.objects.filter(
            Q(start_datetime__gte=day)
            & Q(start_datetime__lt=next_day)
            & event_additional_query),
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
    def as_tree_member(self, leaf):
        if not leaf:
            return None
        if not isinstance(leaf, self.model_class):
            leaf = self.model_class.objects.get(id=leaf.id)
        if leaf.permissions == TagManagementTree.OWNER:
            return leaf
        return None
    def is_last(self, leaf):
        return TagManagementTree.objects.filter(managed=leaf.managed, permissions=TagManagementTree.OWNER).count() == 1

class TagPublishersTreeUtil(BaseManagementTreeUtil):
    def is_manager(self, managed, user):
        logger.info("I'm publisher!")
        return managed.sharers.filter(shared_to=user).exists()
    def is_last(self, leaf):
        """
        leaf: *tournament.models.TagManagementTree* instance.
        returns: there is only one manager for this *Tag*.
        """
        return TagManagementTree.objects.filter(managed=leaf.managed).count() == 1



_base_owners_util = BaseManagementTreeUtil()
tag_owners_util = TagOwnersTreeUtil()
tag_sharers_util = _base_owners_util

def is_owner(managed, user):
    return user.is_authenticated() and _base_owners_util.is_manager(managed, user)

def can_publish_tag(tag, user):
    return user.is_authenticated() and (TagManagementTree.objects.filter(managed=tag, shared_to=user)).exists()


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

class OpenChatFeed(ChatFeed):
    def get_object(self, request, model_key, id):
        return get_object_or_404(KEY_TO_CHAT_OWNER[model_key], id=id)

    def item_link(self, item):
        return reverse('open_chat_message', kwargs={'id': item.id, 'model_key': item.model_key})

    def items(self, obj):
        model_key = CHAT_OWNER_TO_URL_KEY[obj.__class__]
        for item in Message.objects.filter(chat=obj.chat).order_by('-create_time')[:30]:
            item.model_key = model_key
            yield item

    def link(self, obj):
        return reverse('open_rss', kwargs={'model_key': CHAT_OWNER_TO_URL_KEY[obj.__class__], 'id': obj.id})

    def title(self, obj):
        return obj.name

def sort_by_key(iterable, key, reverse=False):
    if sys.version_info >= (3, 0):
        return sorted(iterable, key=key, reverse=reverse)
    return sorted(iterable, lambda x, y: cmp(key(x), key(y)), reverse=reverse)