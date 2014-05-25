from django.db.models import Q

from tournament.models import Tournament, Competition, Participation, Tag, TagManagementTree
from core.decorators import OwnerOnly, InstancePreloaderAndPermissionChecker
from tournament.utils import TagOwnersTreeUtil, TagPublishersTreeUtil, BaseManagementTreeUtil, is_owner, can_publish_tag


class can_modify_participation(OwnerOnly):
    default_get_key = 'participation_id'
    default_set_key = 'participation'

    __name__ = 'can_modify_participation'

    model_class = Participation

    def get_instance_owner(self, instance):
        return instance.competition.owner


class BaseManagerOnly(InstancePreloaderAndPermissionChecker):
    owners_tree_util = BaseManagementTreeUtil()

    def has_permission(self, user, instance):
        return self.owners_tree_util.is_manager(instance, user)



class BaseTagManagerOnly(BaseManagerOnly):
    default_get_key = 'tag_id'
    default_set_key = 'tag'
    model_class = Tag


class tag_owner_only(BaseTagManagerOnly):
    owners_tree_util = TagOwnersTreeUtil()

    __name__ = 'tag_owner_only'


class tag_sharer_and_owner_only(BaseTagManagerOnly):
    __name__ = 'tag_sharer_and_owner_only'

    def has_permission(self, user, instance):
        return can_publish_tag(instance, user)


class tournament_owner_only(BaseManagerOnly):
    default_get_key = 'tournament_id'
    default_set_key = 'tournament'
    model_class = Tournament
    __name__ = 'tournament_owner_only'



class competition_owner_only(BaseManagerOnly):
    default_get_key = 'competition_id'
    default_set_key = 'competition'
    model_class = Competition
    __name__ = 'competition_owner_only'

class can_upgrade_manager(BaseManagerOnly):
    default_get_key = 'manager_id'
    default_set_key = 'manager'
    model_class = TagManagementTree
    __name__ = 'can_upgrade_manager'
    owners_tree_util = TagOwnersTreeUtil()

    def has_permission(self, user, instance):
        return super(can_upgrade_manager, self).has_permission(user, instance.managed)


class BaseTagMasterManagerOnly(BaseManagerOnly):
    default_get_key = 'manager_id'
    default_set_key = 'manager'
    model_class = TagManagementTree

    def has_permission(self, user, instance):
        if instance.shared_to == user and not self.owners_tree_util.is_last(instance):
            return True
        return self.owners_tree_util.find_from_leaf_to_root(instance, user)


class tag_master_owner_only(BaseTagMasterManagerOnly):
    owners_tree_util = TagOwnersTreeUtil()
    __name__ = 'tag_master_owner_only'


class tag_master_sharer_or_owner_only(BaseTagMasterManagerOnly):
    owners_tree_util = TagPublishersTreeUtil()
    __name__ = 'tag_master_sharer_or_owner_only'

    def has_permission(self, user, instance):
        if is_owner(instance.managed, user):
            return True
        return super(tag_master_sharer_or_owner_only, self).has_permission(user, instance)





