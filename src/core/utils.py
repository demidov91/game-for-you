import sys
from datetime import datetime

from collections import deque
from django.core.signals import got_request_exception
from core.models import ShareTree

import logging
logger = logging.getLogger(__name__)


def log(*args, **kwargs):
    logger.exception('Unhandled error.')

got_request_exception.connect(log)



class Adapter(object):
    """
    Wrapper for all object attributes.
    """
    adaptee = None

    def __init__(self, model):
        self.adaptee = model

    def __getattr__(self, attr):
        return getattr(self.adaptee, attr)


class ShareTreeUtil:
    model_class = ShareTree

    def as_tree_member(self, leaf):
        """
        Method that indicates if the *leaf* can be in this sharing tree.
        *leaf* - **core.models.ShareTree** instance.
        """
        return leaf

    def find_from_leaf_to_root(self, leaf, user_to_find):
        """
        returns: *ShareTree* instance with *share_to*==**user_to_find**.
        """
        while leaf.parent:
            if leaf.parent.shared_to == user_to_find:
                return self.as_tree_member(leaf.parent)
            leaf = leaf.parent
        return None

    def is_last(self, leaf):
        """
        *leaf* - **core.models.ShareTree** instance.
        """
        return not (leaf.parent or ShareTree.objects.filter(parent=leaf).exists())

    def is_in_share_tree(self, root, user):
        """
        *user*: user to find in ShareTree.
        *root*: root tree element.
        returns: **bool**.
        """
        return bool(self.find_leaf_by_owner(root, user))

    def find_leaf_by_owner(self, root, user):
        """
        *user*: user to find in ShareTree.
        *root*: root tree element.
        returns: *ShareTree* instance.
        """
        leaves = deque((root,))
        while leaves:
            leaf = leaves.popleft()
            if leaf.shared_to == user:
                return leaf
            leaves.extend(self.model_class.objects.filter(parent=leaf))
        return None

    def get_tree_members(self, root):
        """
        root: *ShareTree* instance.
        returns: *list* of all dependent *ShareTree* leaves starting with **root**.
        """
        plain_tree = []
        leaves = deque((root,))
        while leaves:
            leaf_to_add = leaves.popleft()
            if self.as_tree_member(leaf_to_add):
                plain_tree.append(leaf_to_add)
            leaves.extend(self.model_class.objects.filter(parent=leaf_to_add))
        return plain_tree

share_tree_util = ShareTreeUtil()


def is_in_share_tree(user, share_tree):
    """
    *user*: user to find in ShareTree.
    *share_tree*: root tree element.
    returns: **bool**.
    """
    return share_tree_util.is_in_share_tree(share_tree, user)

def has_higher_priority(user, acceptor, root):
    """
    returns: *bool*.
    """
    acceptor_leaf = find_leave_by_owner(root, acceptor)
    if not acceptor_leaf:
        return True
    return bool(find_from_leaf_to_root(acceptor_leaf, user))

def find_leave_by_owner(root, user):
    """
    *user*: user to find in ShareTree.
    *root*: root tree element.
    returns: *ShareTree* instance.
    """
    return share_tree_util.find_leaf_by_owner(root, user)



def find_from_leaf_to_root(leaf, user_to_find):
    return share_tree_util.find_from_leaf_to_root(leaf, user_to_find)


def get_root(leaf):
    while leaf.parent:
        leaf = leaf.parent
    return leaf

def to_timestamp(date_time):
    """
    date_time: *datetime.datetime* instance.
    returns: *int* - UNIX timestamp.
    """
    if date_time is None:
        return None
    if sys.version_info > (3, 2):
        return date_time.timestamp()
    td = date_time - datetime(1970, 1, 1, tzinfo=date_time.tzinfo)
    return td.days * 24 * 3600 + td.seconds + td.microseconds / 1e6

string_types = str if sys.version_info[0] == 3 else basestring

class Mock:
    pass

class UserMock:
    _is_authenticated = False
    def is_authenticated(self):
        return self._is_authenticated