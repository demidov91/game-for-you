from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from relations.models import Team


class team_owner_only():
    def __init__(self, set_key='team', get_key='team_id'):
        self.set_key = set_key
        self.get_key = get_key

    __name__ = 'team_owner_only'

    def __call__(self, view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            team_id = kwargs.get('team_id')
            team = get_object_or_404(Team.objects, id=team_id)
            if (not team.owner.shared_to == request.user) or (team.owner.shared_to == None and not team.owner.parent_set.filter(shared_to=request.user).exists()):
                return HttpResponseForbidden()
            kwargs[self.set_key] = team
            del kwargs[self.get_key]
            return view_func(request, *args, **kwargs)
        return wrapper



