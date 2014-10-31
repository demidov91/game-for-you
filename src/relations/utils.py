from django.core.urlresolvers import reverse
from django.conf import settings

from relations.models import Team
from relations.decorators import auth_by_get, team_member_only
from core.models import ShareTree
from core.utils import Adapter, is_in_share_tree, has_higher_priority, find_leave_by_owner
from chat.models import Chat
from chat.utils import ChatFeed
from chat.models import Message

import logging
logger = logging.getLogger(__name__)

def create_team(owner):
    """
    Crates team with owner.
    owner: owner User.
    """
    root_owner = ShareTree.objects.create(parent=None, shared_to=owner)
    new_team = Team.objects.create(owner=root_owner, is_draft=True, chat=Chat.objects.create())
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


class TeamChatFeed(ChatFeed):
    @auth_by_get
    @team_member_only(set_key='team')
    def _feed_as_view(request, team):
        """
        This method exists only to use decorators as for view.
        """
        team.owner_key = request.user.userprofile.external_read_auth
        return team

    def get_object(self, request, team_id):
        return TeamChatFeed._feed_as_view(request, team_id=team_id)

    def link(self, obj):
        return '{0}?{1}={2}'.format(
            reverse('team_rss', kwargs={'team_id': obj.id}),
            settings.GET_AUTH_PARAM, obj.owner_key)

    def item_link(self, item):
        return '{0}?{1}={2}'.format(
            reverse('team_chat_message', kwargs={'id': item.id}),
            settings.GET_AUTH_PARAM, item.owner_key)

    def items(self, obj):
        for message in Message.objects.filter(chat=obj.chat).order_by('-create_time')[:30]:
            message.owner_key = obj.owner_key
            yield message

    def title(self, obj):
        return obj.name


