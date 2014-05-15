from collections import deque

from core.models import ShareTree

class Adapter(object):
    """
    Wrapper for all object attributes.
    """
    adaptee = None

    def __init__(self, model):
        self.adaptee = model

    def __getattr__(self, attr):
        return getattr(self.adaptee, attr)

def is_in_share_tree(user, share_tree):
    """
    *user*: user to find in ShareTree.
    *share_tree*: root tree element.
    returns: **bool**.
    """
    return bool(find_leave_by_owner(share_tree, user))

def has_higher_priority(user, acceptor, root):
    """
    returns: *bool*.
    """
    acceptor_leaf = find_leave_by_owner(root, acceptor)
    if not acceptor_leaf:
        return True
    return bool(find_from_leave_to_root(acceptor_leaf, user))

def find_leave_by_owner(root, user):
    """
    *user*: user to find in ShareTree.
    *share_tree*: root tree element.
    returns: *ShareTree* instance.
    """
    leaves = deque((root,))
    while leaves:
        leaf = leaves.popleft()
        if leaf.shared_to == user:
            return leaf
        leaves.extend(ShareTree.objects.filter(parent=leaf))
    return None

def find_from_leave_to_root(leaf, user_to_find):
    while leaf.parent:
        if leaf.parent.shared_to == user_to_find:
            return leaf.parent
        leaf = leaf.parent
    return None

def get_root(leaf):
    while leaf.parent:
        leaf = leaf.parent
    return leaf