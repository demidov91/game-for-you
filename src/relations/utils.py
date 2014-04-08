from relations.models import Team
from core.models import ShareTree


def create_team(owner):
    """
    Crates team with owner.
    owner: owner User.
    """
    root_owner = ShareTree.objects.create(parent=None, shared_to=owner)
    new_team = Team.objects.create(owner=root_owner, is_draft=True)
    new_team.members.add(owner.get_userprofile())
