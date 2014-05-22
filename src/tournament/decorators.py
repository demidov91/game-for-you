from tournament.models import Tournament, Competition, Participation, Tag, TagOwnersTree
from core.decorators import OwnerOnly, InstancePreloaderAndPermissionChecker
from tournament.utils import is_in_management_tree

class tournament_owner_only(OwnerOnly):
    default_get_key = 'tournament_id'
    default_set_key = 'tournament'

    __name__ = 'tournament_owner_only'

    model_class = Tournament


class competition_owner_only(OwnerOnly):
    default_get_key = 'competition_id'
    default_set_key = 'competition'

    __name__ = 'competition_owner_only'

    model_class = Competition

    def get_instance_owner(self, instance):
        return instance.owners

class can_modify_participation(OwnerOnly):
    default_get_key = 'participation_id'
    default_set_key = 'participation'

    __name__ = 'can_modify_participation'

    model_class = Participation

    def get_instance_owner(self, instance):
        return instance.competition.owners


class tag_owner_only(InstancePreloaderAndPermissionChecker):
    default_get_key = 'tag_id'
    default_set_key = 'tag'

    __name__ = 'tag_owner_only'

    model_class = Tag

    def has_permission(self, user, instance):
        return is_in_management_tree(TagOwnersTree, instance, user)