from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

from relations.models import Team
from relations.forms import TeamForm
from relations.decorators import team_owner_only
from relations.utils import create_team


@login_required
def add_team(request):
    """
    Create a new team record and redirect to it's edit page or get draft team created before and edit it.
    """
    just_created_team = Team.objects.filter(Q(is_draft=True), Q(owner__shared_to=request.user) | (Q(owner__shared_to=None) & Q(owner__sharetree__shared_to=request.user)))
    if just_created_team.exists():
        just_created_team = just_created_team.last()
    else:
        just_created_team = create_team(request.user)
    return redirect('edit_team', just_created_team.id)


class EditTeamView(View):
    form_class = TeamForm
    template_name = 'edit_team.html'

    def get(self, request, team):
        return render(request, self.template_name, {'team_form':  TeamForm(instance=team)})

    def post(self, request, team):
        form = self.form_class(request.POST, instance=team)
        if not form.is_valid():
            return render(request, self.template_name, {'team_form': form })
        form.save()
        return redirect('view_team', team.id)

    @method_decorator(team_owner_only())
    def dispatch(self, request, *args, **kwargs):
        return super(EditTeamView, self).dispatch(request, *args, **kwargs)


def view_team(request, team_id):
    team = get_object_or_404(Team.objects, id=team_id)
    return render(request, 'view_team.html', {'team': team})



def view_contacts(request):
    return render(request, 'contacts.html', {'contacts': request.user.known_people.all()})