from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from tournament.models import Tag


@python_2_unicode_compatible
class TagMessage(models.Model):
    class Meta:
        ordering = ('create_time', )
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, default=datetime.now())
    author = models.ForeignKey(get_user_model(), null=False, blank=False)
    tag = models.ForeignKey(Tag, null=False, blank=False)
    
    def __str__(self):
        return u'{0} {1} {2}'.format(self.author.userprofile.get_short_name(), _('for tag'), self.tag.name)