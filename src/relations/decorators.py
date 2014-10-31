from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden

from relations.models import Team, UserProfile
from core.decorators import OwnerOnly, InstancePreloaderAndPermissionChecker

import logging
logger = logging.getLogger(__name__)

class team_owner_only(OwnerOnly):
    default_get_key = 'team_id'
    default_set_key = 'team'

    __name__ = 'team_owner_only'

    model_class = Team

class team_root_owner_only(team_owner_only):
    __name__ = 'team_root_owner_only'

    def has_permission(self, user, instance):
        """
        Checks if the *user* is *Team.owner*.
        """
        return instance.owner.shared_to == user


class team_member_only(InstancePreloaderAndPermissionChecker):
    default_get_key = 'team_id'
    default_set_key = 'team'

    model_class = Team
    __name__ = 'team_member_only'

    def has_permission(self, user, instance):
        return user.userprofile and instance.members.filter(id=user.userprofile.id)

def auth_by_get(view_func):
    """
    Authenticates request by **settings.GET_AUTH_PARAM** get parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated() and settings.GET_AUTH_PARAM in request.GET:
            try:
                profile = UserProfile.objects.get(external_read_auth=request.GET[settings.GET_AUTH_PARAM])
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden()
            if not profile.user:
                return HttpResponseForbidden()
            request.user = profile.user
        return view_func(request, *args, **kwargs)
    return wrapper


