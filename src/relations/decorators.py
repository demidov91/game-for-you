from relations.models import Team
from core.decorators import OwnerOnly, InstancePreloaderAndPermissionChecker

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



