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
    leaves = deque((share_tree,))
    while leaves:
        leave = leaves.popleft()
        if leave.shared_to == user:
            return True
        leaves.extend(ShareTree.objects.filter(parent=leave))
    return False
