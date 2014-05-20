from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ShareTree(models.Model):
    parent = models.ForeignKey('core.ShareTree', null=True)
    shared_to = models.ForeignKey('auth.User', related_name='shared_to')

    def delete(self, using=None):
        ShareTree.objects.filter(parent=self).update(parent=self.parent)
        super(ShareTree, self).delete(using)

    def __str__(self):
        if self.parent:
            return u'id {0}, {1}. {2} {3} (id:{4})'.format(
                self.id, self.shared_to, _('Depends on'), self.parent.shared_to, self.parent.id)
        return  u'id {0}, {1}. {2}.'.format(self.id, self.shared_to, _('Root element'))