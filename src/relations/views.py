from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from relations.models import Team, UserProfile, UserContact
from relations.forms import TeamForm, ProfileSettings
from relations.decorators import team_owner_only, team_member_only
from relations.utils import create_team, can_delete_team, get_members_for_editor
from core.utils import is_in_share_tree, has_higher_priority, find_leave_by_owner, find_from_leave_to_root, get_root
from core.models import ShareTree
from tournament.forms import UserPlacesFormset


@login_required
def add_team(request):
    """
    Create a new team record and redirect to it's edit page or get draft team created before and edit it.
    """
    just_created_team = Team.objects.filter(Q(is_draft=True), Q(owner__shared_to=request.user) | (Q(owner__shared_to=None) & Q(owner__sharetree__shared_to=request.user)))
    if just_created_team.exists():
        just_created_team = just_created_team[0]
    else:
        just_created_team = create_team(request.user)
    return redirect('edit_team', just_created_team.id)


class EditTeamView(View):
    form_class = TeamForm
    template_name = 'edit_team.html'

    def get(self, request, team):
        return render(request, self.template_name, {
            'team_form':  TeamForm(instance=team),
            'team': team,
            'members': get_members_for_editor(team, request.user),
            'contacts': request.user.known_people.all(),
        })

    def post(self, request, team):
        form = self.form_class(request.POST, instance=team)
        if not form.is_valid():
            return render(request, self.template_name, {
                'team_form': form,
                'team': team,
                'members': get_members_for_editor(team, request.user),
                'contacts': request.user.known_people.all(),
            })
        form.save()
        return redirect('view_team', team.id)

    @method_decorator(team_owner_only())
    def dispatch(self, request, *args, **kwargs):
        return super(EditTeamView, self).dispatch(request, *args, **kwargs)

@team_member_only(set_key='team')
def view_team(request, team):
    return render(request, 'view_team.html', {
        'team': team,
        'is_owner': is_in_share_tree(request.user, team.owner)
    })


@team_owner_only(set_key='team')
@require_POST
def delete_team(request, team):
    if can_delete_team(request.user, team):
        team.delete()
    return redirect('index')


def view_contacts(request):
    return render(request, 'contacts.html', {'contacts': request.user.known_people.all()})


def find_by_name(request):
    contains = request.GET.get('contains')
    people = UserProfile.objects.filter(
        Q(patronymic__icontains=contains) |
        Q(user__first_name__icontains=contains) |
        Q(user__last_name__icontains=contains) |
        Q(user__username__icontains=contains)
    ).distinct()
    return render(request, 'parts/found_people.html', {
        'people': people,
    })

@require_POST
@login_required
def add_contact(request):
    userprofile = get_object_or_404(UserProfile.objects, id=request.POST.get('userprofile_id'))
    UserContact.objects.get_or_create(owner=request.user, about=userprofile)
    return render(request, 'parts/contacts_list.html', {
        'contacts': request.user.known_people.all(),
    })

@require_POST
@login_required
def remove_contact(request, contact_id):
    contact = get_object_or_404(UserContact.objects, id=contact_id, owner=request.user)
    contact.delete()
    return render(request, 'parts/contacts_list.html', {
        'contacts': request.user.known_people.all(),
    })

@require_POST
@login_required
def remove_team_member(request, userprofile_id, team_id):
    team = get_object_or_404(Team.objects, id=team_id)
    acceptor = get_object_or_404(UserProfile.objects, id=userprofile_id)
    if not has_higher_priority(request.user, acceptor, team.owner):
        return HttpResponseForbidden()
    team.members.remove(acceptor)
    return render(request, 'parts/team_members.html', {
        'members': get_members_for_editor(team, request.user),
        'team': team,
    })

@require_POST
@team_owner_only(set_key='team')
def add_team_member(request, userprofile_id, team):
    acceptor = get_object_or_404(UserProfile.objects, id=userprofile_id)
    team.members.add(acceptor)
    return render(request, 'parts/team_members.html', {
        'members': get_members_for_editor(team, request.user),
        'team': team,
    })

@require_POST
@team_owner_only(set_key='team')
def make_team_owner(request, userprofile_id, team):
    acceptor = get_object_or_404(UserProfile.objects, id=userprofile_id)
    if not acceptor.user or is_in_share_tree(acceptor.user, team.owner):
        return HttpResponseForbidden()
    parent_leave = find_leave_by_owner(team.owner, request.user)
    ShareTree.objects.create(shared_to=acceptor.user, parent=parent_leave)
    return render(request, 'parts/team_members.html', {
        'members': get_members_for_editor(team, request.user),
        'team': team,
    })

@require_POST
@login_required
def undo_team_owner(request, share_tree_id):
    leaf = get_object_or_404(ShareTree.objects, id=share_tree_id)
    my_leaf = find_from_leave_to_root(leaf, request.user)
    if my_leaf:
        leaf.delete()
        root = get_root(my_leaf)
        team = Team.objects.get(owner=root)
        return render(request, 'parts/team_members.html', {
            'members': get_members_for_editor(team, request.user),
            'team': team,
        })
    return HttpResponseForbidden()

@login_required
def view_settings(request, update_places=False, update_user=False):
    if request.method == 'POST' and update_user:
        profile_settings = ProfileSettings(instance=request.user.userprofile, data=request.POST)
        if profile_settings.is_valid():
            profile_settings.save()
            return redirect('settings')
    else:
        profile_settings = ProfileSettings(instance=request.user.userprofile)
    if request.method == 'POST' and update_places:
        places = UserPlacesFormset(owner=request.user, data=request.POST)
        if places.is_valid():
            places.save()
            return redirect('settings')
    else:
        places = UserPlacesFormset(owner=request.user)
    return render(request, 'settings.html', {
        'profile_form': profile_settings,
        'places_formset': places,
        'known_places': places.queryset,
    })
