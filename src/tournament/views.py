import json
from datetime import datetime

from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q

from tournament.utils import get_tags, get_calendar_events_by_tags, get_events_by_tags_and_day, get_default_participation_state
from tournament.forms import TournamentForm, AddCompetitionForm
from tournament.models import Competition, Participation
from relations.models import Team
from core.utils import is_in_share_tree


def _unauthenticated_view(request):
    tags = get_tags(request)
    return render(request, 'unauthenticated_index.html', {
        'tags': tags,
        'show_login': 'force-login' in request.GET,
        'redirect_after_login': request.GET.get('next'),
        })

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
        'tournament_form': TournamentForm(request.GET),
        'competition_form': AddCompetitionForm(request.GET),
        })


@require_POST
@login_required
def add_tournament(request):
    form = TournamentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_event.html',  {
        'tournament_form': form,
        'competition_form': AddCompetitionForm(),
        })


@require_POST
@login_required
def add_competition(request):
    form = AddCompetitionForm(request.POST, owner=request.user)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_event.html',  {
        'tournament_form': TournamentForm(),
        'competition_form': form,
        })


def view_competition(request, competition_id):
    competition = get_object_or_404(Competition.objects, id=competition_id)
    approved_participants = Participation.objects.filter(
        competition=competition,
        state=Participation.APPROVED)
    template_name = 'competition.html' if request.user.is_authenticated() else 'unauthenticated_competition.html'
    context = {
        'competition': competition,
        'approved_participants': approved_participants,
        'claimants': Team.objects.filter(id__in=Participation.objects.filter(
            competition=competition,
            state=Participation.CLAIM).values_list('id', flat=True)),
        'user_teams_id': [],
    }
    if request.user.is_authenticated():
        is_competition_owner = is_in_share_tree(request.user, competition.owners)
        if is_competition_owner:
            context.update({
               'declined_claimants': Participation.objects.filter(competition=competition, state=Participation.DECLINED),
            })
        context['user_teams_id'] = request.user.userprofile.teams.values_list('id', flat=True)
        context.update({
            'teams_to_add': request.user.userprofile.teams.filter(is_draft=False).exclude(
                id__in=Participation.objects.filter(
                    Q(competition=competition_id)).values_list('team_id', flat=True)),
            'is_competition_owner': is_competition_owner,
        })
    else:
        context.update({
            'redirect_after_login': reverse('view_competition', kwargs={'competition_id': competition_id}),
        })
    return render(request, template_name, context)


@require_POST
@login_required
def add_participation_request(request, competition_id):
    """
    AJAX view. Returns 403 or json with key state set to *Participation.state* value.
    """
    try:
        team = request.user.userprofile.teams.get(id=request.POST.get('team_id'))
        competition = Competition.objects.get(id=competition_id)
    except (Team.DoesNotExist, Competition.DoesNotExist):
        return HttpResponseForbidden(_('Wrong request data.'))
    participation = Participation.objects.create(
        team=team,
        competition=competition,
        creator=request.user,
        state=get_default_participation_state(competition))
    return HttpResponse(json.dumps({'state': participation.state }), content_type='application/json')

@require_POST
@login_required
def undo_participation_request(request, participation_id):
    participation = get_object_or_404(Participation.objects, id=participation_id)
    if request.user.userprofile.teams.filter(id=participation.team.id).exists():
        participation.delete()
        return HttpResponse()
    if is_in_share_tree(request.user, participation.competition.owners):
        participation.state = Participation.DECLINED
        participation.save()
        return HttpResponse()
    return HttpResponseForbidden()

@require_POST
@login_required
def accept_participation_request(request, participation_id):
    participation = get_object_or_404(Participation.objects, id=participation_id)
    if not is_in_share_tree(request.user, participation.competition.owners):
        return HttpResponseForbidden()
    participation.state = Participation.APPROVED
    participation.save()
    return HttpResponse()
