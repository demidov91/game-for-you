from datetime import timedelta

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.conf import settings

from tournament.models import Tag, Tournament, Competition, Participation


def get_default_tag_ids(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators
    returns: **tuple** of **int**.
    """
    return settings.DEFAULT_TAGS



def _get_tags_for_none_authenticated(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators.
    returns: collection of *Tag*
    """
    tags = request.session.get('tags')
    if tags is None:
        tags = get_default_tag_ids(request)
        request.session['tags'] = tags
    return Tag.objects.filter(id__in=tags)

def get_tags(request):
    """
    returns: Tags for authenticated and none authenticated users.
    """
    if request.user.is_authenticated():
        return request.user.subscribed_to.all()
    else:
        return _get_tags_for_none_authenticated(request)


def get_calendar_events_by_tags(tags, start, end):
    tournaments = Tournament.objects.filter(Q(tags=tags) & Q(last_datetime__range=(start, end)) | Q(first_datetime__range=(start, end))).distinct()
    competitions = Competition.objects.filter(tags=tags, start_datetime__range=(start, end))
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
        'tournaments': Tournament.objects.filter(tags=tags, first_datetime__lte=day, last_datetime__gte=day),
        'competitions':  Competition.objects.filter(tags=tags,
                                                    start_datetime__gte=day,
                                                    start_datetime__lt=next_day),
    }

def tournaments_to_calendar_events(tournaments):
    return tuple({
        'title': t.name,
        'start': t.first_datetime.timestamp(),
        'end': t.last_datetime.timestamp(),
        'url': reverse('view_tournament', kwargs={'tournament_id': t.id, })
    } for t in tournaments)

def competitions_to_calendar_events(competitions):
    return tuple({
        'title': c.get_name(),
        'start': c.start_datetime.timestamp(),
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





