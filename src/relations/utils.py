from relations.models import Team
from core.models import ShareTree
from core.utils import Adapter, is_in_share_tree, has_higher_priority, find_leave_by_owner


def create_team(owner):
    """
    Crates team with owner.
    owner: owner User.
    """
    root_owner = ShareTree.objects.create(parent=None, shared_to=owner)
    new_team = Team.objects.create(owner=root_owner, is_draft=True)
    new_team.members.add(owner.userprofile)
    new_team.save()
    if not owner.userprofile.primary_team:
        owner.userprofile.primary_team = new_team
        owner.userprofile.save()
    return new_team


def can_delete_team(user, group):
    """
    if *user* is the last *group* owner.
    user: **auth.User**
    group: Team or Tag. It should have *owner* field of **ShareTree** type.
    returns: True/False.
    """
    return group.owner.shared_to == user


class TeamMemberForEditor(Adapter):
    def __init__(self, team, instance, editor):
        super(TeamMemberForEditor, self).__init__(instance)
        self.editor = editor
        self.team = team

    def is_owner(self):
        return self.adaptee.user and is_in_share_tree(self.adaptee.user, self.team.owner)

    def can_undo_owner(self):
        return has_higher_priority(self.editor, self.adaptee.user, self.team.owner)

    def get_leave(self):
        return find_leave_by_owner(self.team.owner, self.adaptee.user)


def get_members_for_editor(team, editor):
    return tuple(TeamMemberForEditor(team, member, editor) for member in team.members.all())


