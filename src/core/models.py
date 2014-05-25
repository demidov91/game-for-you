import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


def get_models_super_string(instance):
    """
    Helper function to get string representation of the super model class in python version independent way.
    """
    model_class = instance.__class__
    if sys.version_info[0] > 2:
        return super(model_class, instance).__str__()
    else:
        return force_text(super(model_class, instance))


@python_2_unicode_compatible
class ShareTree(models.Model):
    parent = models.ForeignKey('core.ShareTree', null=True, blank=True)
    shared_to = models.ForeignKey('auth.User', related_name='shared_to')

    def remove_from_tree(self):
        """
        Moves all incoming connections to the *parent*.
        """
        ShareTree.objects.filter(parent=self).update(parent=self.parent)

    def delete(self, using=None):
        self.remove_from_tree()
        super(ShareTree, self).delete(using)

    def __str__(self):
        if self.parent:
            return u'id {0}, {1}. {2} {3} (id:{4})'.format(
                self.id, self.shared_to, _('Depends on'), self.parent.shared_to, self.parent.id)
        return  u'id {0}, {1}. {2}.'.format(self.id, self.shared_to, _('Root element'))