import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from tournament.utils import get_tags, get_calendar_events_by_tags, get_events_by_tags_and_day
from tournament.forms import TournamentForm, CompetitionForm


def _unauthenticated_view(request):
    tags = get_tags(request)
    return render(request, 'unauthenticated_index.html', {'tags': tags})

def _authenticated_index(request):
    return render(request, 'index.html', {'tags': request.user.subscribed_to.all()})


def index(request):
    """
    'Calendar' page. Processes both authenticated and none-authenticated requests.
    """
    return _authenticated_index(request) if request.user.is_authenticated() else _unauthenticated_view(request)


@require_GET
def calendar_events_json(request):
    start = datetime.fromtimestamp(int(request.GET['start']))
    end = datetime.fromtimestamp(int(request.GET['end']))
    tags = get_tags(request)
    data = json.dumps(get_calendar_events_by_tags(tags, start, end))
    return HttpResponse(data, content_type='application/json')


@require_GET
def calendar_events_for_day_ajax(request):
    date = datetime(day=int(request.GET.get('day')), month=int(request.GET.get('month')), year=int(request.GET.get('year')))
    tags = get_tags(request)
    return render(request, 'parts/events_for_day.html', get_events_by_tags_and_day(tags, date))


@require_GET
@login_required
def add_event(request):
    return render(request, 'add_event.html', {
        'tournament_form': TournamentForm(),
        'competition_form': CompetitionForm(),
        })


@require_POST
@login_required
def add_tournament(request):
    form = TournamentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_event',  {
        'tournament_form': form,
        'competition_form': CompetitionForm(),
        })


@require_POST
@login_required
def add_competition(request):
    form = CompetitionForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_event',  {
        'tournament_form': TournamentForm(),
        'competition_form': form,
        })