import json

from django.http import HttpResponse
from django.shortcuts import render

from tournament.utils import get_default_tags, get_calendar_events_from_db, get_calendar_events_from_cookies
from tournament.models import Tag


def _unauthenticated_view(request):
    tags = get_default_tags(request)
    return render(request, 'unauthenticated_index.html', {'tags': tags})

def _authenticated_index(request):
    return render(request, 'index.html', {'tags': request.user.subscribed_to})


def index(request):
    """
    'Calendar' page. Processes both authenticated and none-authenticated requests.
    """
    return _authenticated_index(request) if request.user.is_authenticated() else _unauthenticated_view(request)



def calendar_events_json(request):
    data = json.dumps({
        'events': get_calendar_events_from_db() if request.user.is_authenticated() else get_calendar_events_from_cookies()
    })
    return HttpResponse(data, content_type='application/json')

