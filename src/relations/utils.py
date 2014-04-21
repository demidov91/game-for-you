from relations.models import Team
from core.models import ShareTree


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
    if group.owner.shared_to == user:
        return True
    return False

