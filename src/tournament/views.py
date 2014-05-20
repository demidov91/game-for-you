import json
from datetime import datetime
import time

from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q

from tournament.utils import get_tags, get_calendar_events_by_tags, get_events_by_tags_and_day,\
    get_default_participation_state, get_calendar_events_by_team
from tournament.forms import TournamentForm, AddCompetitionForm
from tournament.models import Competition, Participation, Tournament
from tournament.decorators import tournament_owner_only, competition_owner_only, can_modify_participation
from relations.models import Team
from core.utils import is_in_share_tree, to_timestamp


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
def calendar_events_for_team_json(request, team_id):
    start = datetime.fromtimestamp(int(request.GET['start']))
    end = datetime.fromtimestamp(int(request.GET['end']))
    team = get_object_or_404(request.user.userprofile.teams, id=team_id)
    data = json.dumps(get_calendar_events_by_team(team, start, end))
    return HttpResponse(data, content_type='application/json')


@require_GET
@login_required
def add_event(request):
    initial = dict(request.GET)
    start_datetime = initial.get('default_date') or (time.time(), )
    if start_datetime:
        initial['start_datetime'] = initial['first_datetime'] = initial['last_datetime'] =\
            datetime.fromtimestamp(int(start_datetime[0]))
    tournament = initial.get('tournament')
    if tournament:
        initial['tournament'] = tournament[0]

    return render(request, 'add_event.html', {
        'tournament_form': TournamentForm(initial=initial),
        'competition_form': AddCompetitionForm(initial=initial, owner=request.user),
        })


@require_POST
@login_required
def add_tournament(request):
    form = TournamentForm(request.POST)
    if form.is_valid():
        form.save(request.user)
        return redirect('index')
    return render(request, 'add_event.html',  {
        'tournament_form': form,
        'competition_form': AddCompetitionForm(owner=request.user),
        'show_tournament': True,
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
    template_name = 'competition.html' if request.user.is_authenticated() else 'unauthenticated_competition.html'
    context = {
        'competition': competition,
    }
    if request.user.is_authenticated():
        context['is_competition_owner'] = is_in_share_tree(request.user, competition.owners)
    else:
        context['redirect_after_login'] = reverse('view_competition', kwargs={'competition_id': competition_id})
    return render(request, template_name, context)

def view_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament.objects, id=tournament_id)
    template_name = 'authenticated_tournament.html' if request.user.is_authenticated() else 'unauthenticated_tournament.html'
    default_competition_start = int(max(to_timestamp(tournament.first_datetime), to_timestamp(datetime.now())))
    return render(request, template_name, {
        'tournament': tournament,
        'is_owner': is_in_share_tree(request.user, tournament.owner),
        'default_competition_start': default_competition_start,
    })


@require_POST
@login_required
def add_participation_request(request, competition_id):
    """
    AJAX view. Returns 403 or json with key state set to *Participation.state* value.
    """
    try:
        print((request.POST.get('team_id'), competition_id))
        team = request.user.userprofile.teams.get(id=request.POST.get('team_id'))
        competition = Competition.objects.get(id=competition_id)
    except (Team.DoesNotExist, Competition.DoesNotExist):
        return HttpResponseForbidden(_('Wrong request data.'))
    participation = Participation.objects.create(
        team=team,
        competition=competition,
        creator=request.user,
        state=get_default_participation_state(competition))
    return redirect('view_competition_part', competition_id=participation.competition.id)

@require_POST
@login_required
def undo_participation_request(request, participation_id):
    participation = get_object_or_404(Participation.objects, id=participation_id)
    if request.user.userprofile.teams.filter(id=participation.team.id).exists():
        participation.delete()
        return redirect('view_competition_part', competition_id=participation.competition.id)
    return HttpResponseForbidden()

@require_POST
@can_modify_participation(set_key='participation')
def manage_participation_request(request, participation, state):
    participation.state = state
    participation.save()
    return redirect('view_competition_part', competition_id=participation.competition.id)

def view_competition_part(request, competition_id):
    competition = get_object_or_404(Competition.objects, id=competition_id)
    context = {
        'competition': competition,
        'approved_participants': Participation.objects.filter(
            competition=competition,
            state=Participation.APPROVED),
    }
    if request.user.is_authenticated():
        is_competition_owner = is_in_share_tree(request.user, competition.owners)
        claims = Participation.objects.filter(competition=competition, state=Participation.CLAIM)
        declined_claims = Participation.objects.filter(competition=competition, state=Participation.DECLINED)
        if not is_competition_owner:
            claims = claims.filter(team__in=request.user.userprofile.teams.all())
            declined_claims = declined_claims.filter(team__in=request.user.userprofile.teams.all())
        context['claims'] = claims
        context['declined_claims'] = declined_claims
        context['user_teams_id'] = request.user.userprofile.teams.values_list('id', flat=True)
        context.update({
            'teams_to_add': request.user.userprofile.teams.filter(is_draft=False).exclude(
                id__in=Participation.objects.filter(
                    Q(competition=competition_id)).values_list('team_id', flat=True)),
            'is_competition_owner': is_competition_owner,
        })
    return render(request, 'parts/competition_dynamic.html', context)


@require_POST
@tournament_owner_only(set_key='tournament')
def delete_tournament(request, tournament):
    tournament.delete()
    return redirect('index')


@require_POST
@competition_owner_only(set_key='competition')
def delete_competition(request, competition):
    competition.delete()
    return redirect('index')

