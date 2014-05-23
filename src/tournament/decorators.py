from tournament.models import Tournament, Competition, Participation, Tag, TagManagementTree
from core.decorators import OwnerOnly, InstancePreloaderAndPermissionChecker
from core.utils import ShareTreeUtil
from tournament.utils import TagOwnersTreeUtil

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


class BaseTagManagerOnly(InstancePreloaderAndPermissionChecker):
    default_get_key = 'tag_id'
    default_set_key = 'tag'
    model_class = Tag

    _permission_to_check = None

    def has_permission(self, user, instance):
        return TagManagementTree.objects.filter(
            managed=instance,
            shared_to=user,
            permissions=self._permission_to_check).exists()


class tag_owner_only(BaseTagManagerOnly):
    __name__ = 'tag_owner_only'
    _permission_to_check = TagManagementTree.OWNER


class tag_sharer_only(BaseTagManagerOnly):
    __name__ = 'tag_sharer_only'
    _permission_to_check = TagManagementTree.PUBLISHER



class BaseTagMasterManagerOnly(InstancePreloaderAndPermissionChecker):
    default_get_key = 'manager_id'
    default_set_key = 'manager'
    model_class = TagManagementTree

    share_tree_util = ShareTreeUtil()

    def has_permission(self, user, instance):
        return self.share_tree_util.find_from_leaf_to_root(instance, user)

class tag_master_owner_only(BaseTagMasterManagerOnly):
    share_tree_util = TagOwnersTreeUtil()

    __name__ = 'tag_master_owner_only'


class tag_master_sharer_or_owner_only(BaseTagMasterManagerOnly):
    def has_permission(self, user, instance):
        if instance.managed.owners.filter(shared_to=user).exists():
            return True
        return super(tag_master_sharer_or_owner_only, self).has_permission(user, instance)

    __name__ = 'tag_master_sharer_or_owner_only'



