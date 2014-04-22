from django.db.models import Q

from tournament.models import Tag, Tournament, Competition


def get_default_tag_ids(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators
    returns: **tuple** of **int**.
    """
    return 1,



def _get_tags_for_none_authenticated(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators.
    returns: collection of *Tag*
    """
    tags = request.session.get('tags')
    if not tags:
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
    tournaments = Tournament.objects.filter(Q(tags=tags) & Q(first_datetime__gte=start) | Q(last_datetime__lte=end))
    competitions = Competition.objects.filter(tags=tags, start_datetime__range=(start, end))
    events = []
    events += tournaments_to_calendar_events(tournaments)
    events += competitions_to_calendar_events(competitions)
    return events


def get_events_by_tags_and_day(tags, day):
    return {
        'tournaments': Tournament.objects.filter(Q(tags=tags) & Q(first_datetime__lte=day) | Q(last_datetime__gte=day)),
        'competitions':  Competition.objects.filter(tags=tags, start_datetime=day),
    }

def tournaments_to_calendar_events(tournaments):
    return tuple({
        'title': t.name,
        'start': t.first_datetime,
        'end': t.last_datetime,
    } for t in tournaments)

def competitions_to_calendar_events(competitions):
    return tuple({
        'title': c.name,
        'start': c.start_datetime,
    } for c in competitions)

