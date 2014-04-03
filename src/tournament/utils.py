from tournament.models import Tag


def get_default_tags(request):
    """
    This method is supposed to return default tags by host.
    Maybe, it'll be something else or there will be more indicators.
    """
    return Tag.objects.filter(id__in=(1,))


def get_calendar_events_from_db():
    pass

def get_calendar_events_from_cookies():
    pass