import json
from datetime import datetime
import time

from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from tournament.utils import get_calendar_events_by_tags, get_events_by_tags_and_day,\
    get_default_participation_state, get_calendar_events_by_team, get_tags_provider, is_owner, can_publish_tag,\
    sort_by_key, tag_owners_util
from tournament.forms import TournamentForm, AddCompetitionForm, TagForm
from tournament.models import Competition, Participation, Tournament, Tag, TagManagementTree
from tournament.decorators import tournament_owner_only, competition_owner_only, can_modify_participation,\
    tag_owner_only, tag_master_sharer_or_owner_only, tag_master_owner_only, tag_sharer_and_owner_only,\
    can_upgrade_manager
from relations.models import Team
from core.utils import to_timestamp, share_tree_util
from chat.forms import MessageForm
from chat.utils import get_chat_page

import logging
logger = logging.getLogger(__name__)


def _unauthenticated_view(request):
    tags = get_tags_provider(request).get_tags()
    return render(request, 'unauthenticated_index.html', {
        'tags': tags,
        'show_login': 'force-login' in request.GET,
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
    tag_provider = get_tags_provider(request)
    tags = tag_provider.get_tags()
    data = json.dumps(get_calendar_events_by_tags(tags, start, end, request.user if tag_provider.show_draft() else None))
    return HttpResponse(data, content_type='application/json')


@require_GET
def calendar_events_for_day_ajax(request):
    date = datetime(day=int(request.GET.get('day')), month=int(request.GET.get('month')), year=int(request.GET.get('year')))
    tags = get_tags_provider(request).get_tags()
    return render(request, 'parts/events_for_day.html', get_events_by_tags_and_day(tags, date, request.user))

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
        'tournament_form': TournamentForm(owner=request.user, initial=initial),
        'competition_form': AddCompetitionForm(initial=initial, owner=request.user),
        })


@tournament_owner_only(set_key='tournament')
def edit_tournament(request, tournament):
    if request.method == 'GET':
        form = TournamentForm(owner=request.user, instance=tournament)
    else:
        form = TournamentForm(owner=request.user, instance=tournament, data=request.POST)
        if form.is_valid():
            return redirect('view_tournament', tournament_id=form.save().id)
    return render(request, 'tournament_edit.html', {
        'form': form,
    })

@competition_owner_only(set_key='competition')
def edit_competition(request, competition):
    if request.method == 'GET':
        form = AddCompetitionForm(owner=request.user, instance=competition)
    else:
        form = AddCompetitionForm(owner=request.user, instance=competition, data=request.POST)
        if form.is_valid():
            return redirect('view_competition', competition_id=form.save().id)
    return render(request, 'competition_edit.html', {
        'form': form,
    })

@require_POST
@login_required
def add_tournament(request):
    form = TournamentForm(owner=request.user, data=request.POST)
    if form.is_valid():
        instance = form.save()
        return redirect('view_tournament', tournament_id=instance.id)
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
        'tournament_form': TournamentForm(owner=request.user),
        'competition_form': form,
        })


def view_competition(request, competition_id):
    competition = get_object_or_404(Competition.objects, id=competition_id)
    template_name = 'competition.html' if request.user.is_authenticated() else 'unauthenticated_competition.html'
    context = {
        'competition': competition,
    }
    if request.user.is_authenticated():
        context['is_competition_owner'] = is_owner(competition, request.user)
    return render(request, template_name, context)

def view_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament.objects, id=tournament_id)
    template_name = 'authenticated_tournament.html' if request.user.is_authenticated() else 'unauthenticated_tournament.html'
    default_competition_start = int(max(to_timestamp(tournament.first_datetime), to_timestamp(datetime.now())))
    return render(request, template_name, {
        'tournament': tournament,
        'is_owner': is_owner(tournament, request.user),
        'default_competition_start': default_competition_start,
    })


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
        is_competition_owner = is_owner(competition, request.user)
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

@require_POST
def change_tag_subscription_state(request, subscribe):
    tags_provider = get_tags_provider(request)
    if subscribe:
        tags_provider.add_tag_by_name(request.POST.get('name'))
    else:
        tags_provider.remove_tag_by_id(int(request.POST.get('id')))
    return redirect('index')

@require_GET
def tag_page(request, tag_id):
    tag = get_object_or_404(Tag.objects, id=tag_id)
    template_name = 'tag_authenticated.html' if request.user.is_authenticated() else 'tag_unauthenticated.html'
    context = {
        'tag': tag,
        'is_owner': is_owner(tag, request.user),
        'is_publisher': can_publish_tag(tag, request.user),
        'page_number': request.GET.get('page'),
    }
    if context['is_publisher']:
        tournament_requests = Tournament.objects.filter(tags_request__in=(tag, ))
        competition_requests = Competition.objects.filter(tags_request__in=(tag, ))
        events = list(tournament_requests)
        events.extend(competition_requests)
        events = sort_by_key(events, lambda x: x.create_time, reverse=True)
        context.update({
            'tag_requests': events,
        })
    return render(request, template_name, context)

@require_GET
def get_tag_names(request):
    contains = request.GET.get('term')[0]
    if not contains:
        raise Http404()
    data = tuple(Tag.objects.filter(name__icontains=contains).values_list('name', flat=True))
    return HttpResponse(json.dumps(data), content_type='application/json')


@tag_sharer_and_owner_only(set_key='tag')
def edit_tag(request, tag):
    is_owner = tag_owners_util.is_manager(tag, request.user)
    form = None
    if is_owner:
        if request.method == 'GET':
            form = TagForm(instance=tag)
        else:
            form = TagForm(instance=tag, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('tag_page', tag_id=tag.id)
    return render(request, 'tag_edit.html', {
        'form': form,
        'is_last_owner': is_owner and tag.owners.count() == 1,
        'contacts': request.user.known_people.all(),
        'tag': tag,
        'is_owner': is_owner,
    })

@require_POST
@tag_owner_only(set_key='tag')
def delete_tag(request, tag):
    if tag.owners.all().count() != 1:
        return HttpResponseForbidden(_('Only the last owner can remove tags.'))
    tag.delete()
    return redirect('index')

@require_GET
@tag_owner_only(set_key='tag')
def get_tag_managers_list(request, tag):
    me = TagManagementTree.objects.get(managed=tag, shared_to=request.user)
    dependent_owners = tag_owners_util.get_tree_members(me)[1:]
    independent_owners = tag.owners.exclude(id__in=tuple(x.id for x in dependent_owners)).exclude(id=me.id)
    return render(request, 'parts/tag_managers_list.html', {
        'independent_owners': independent_owners,
        'me_as_owner': me,
        'dependent_owners': dependent_owners,
        'is_last_owner': independent_owners.count() + len(dependent_owners) == 0,
        'sharers': tag.sharers.all(),
    })

@require_GET
@tag_sharer_and_owner_only(set_key='tag')
def get_tag_publishers_list(request, tag):
    me = TagManagementTree.objects.get(managed=tag, shared_to=request.user)
    dependent_owners = share_tree_util.get_tree_members(me)[1:]
    independent_owners = tag.managers.exclude(id__in=tuple(x.id for x in dependent_owners)).exclude(id=me.id)
    return render(request, 'parts/tag_managers_list.html', {
        'independent_owners': independent_owners,
        'sharers': dependent_owners,
        'me_as_owner': me,
    })

@require_POST
@tag_sharer_and_owner_only(set_key='tag')
def add_tag_sharer(request, tag, user_id):
    """
    Use one of the *BaseTagManagerOnly* decorator around this view.
    """
    parent_leaf = get_object_or_404(TagManagementTree.objects, managed=tag, shared_to=request.user)
    new_owner = get_object_or_404(get_user_model(), id=user_id)
    if TagManagementTree.objects.filter(managed=tag, shared_to=new_owner).exists():
        return HttpResponseForbidden()
    TagManagementTree.objects.create(
        managed=tag,
        parent=parent_leaf,
        shared_to=new_owner,
        permissions=TagManagementTree.PUBLISHER)
    return redirect('tag_managers_list', tag_id=tag.id)

@require_POST
@can_upgrade_manager(set_key='manager')
def make_tag_owner(request, manager):
    manager.permissions = TagManagementTree.OWNER
    manager.save()
    return HttpResponse()


@require_POST
@tag_master_owner_only(set_key='manager')
def downgrade_to_tag_sharer(request, manager):
    me_as_leaf = TagManagementTree.objects.get(shared_to=request.user, managed=manager.managed)
    TagManagementTree.objects.filter(parent=manager, permissions=TagManagementTree.OWNER).\
        update(parent=me_as_leaf.parent)
    manager.permissions = TagManagementTree.PUBLISHER
    manager.save()
    return HttpResponse()

@require_POST
@tag_master_sharer_or_owner_only(set_key='tag_manager')
def remove_tag_sharer(request, tag_manager):
    tag_manager.delete()
    if request.is_ajax():
        return HttpResponse()
    return redirect('tag_page', tag_id=tag_manager.managed.id)

@require_POST
@tag_sharer_and_owner_only(set_key='tag')
def accept_tag_request(request, tag, event_id, event_model_class):
    event = get_object_or_404(event_model_class.objects, id=event_id)
    event.tags.add(tag)
    event.tags_request.remove(tag)
    return redirect('tag_page', tag_id=tag.id)

def tag_chat(request, tag_id):
    """
    ajax view.
    request: POST for new message. GET accepts *page* parameter.
    returns: chat part of the tag page.
    """
    tag = get_object_or_404(Tag.objects, id=tag_id)
    chat = tag.chat
    if not chat:
        raise Http404()
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        form = MessageForm(request.POST, request.user, chat)
        if form.is_valid():
            form.save()
            return redirect('tag_chat', tag_id=tag.id)
    else:
        form = MessageForm()
    chat.url = reverse('tag_chat', kwargs={'tag_id': tag_id})
    return render(request, 'parts/chat_message_list.html', {
        'form': form,
        'chat': chat,
        'page': get_chat_page(chat, request.GET.get('page')),
        'is_authenticated': request.user.is_authenticated,
    })