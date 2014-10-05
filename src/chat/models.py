from datetime import datetime

from ckeditor.fields import RichTextField

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Chat(models.Model):
    pass

@python_2_unicode_compatible
class Message(models.Model):
    class Meta:
        ordering = ('create_time', )
    text = RichTextField(config_name='chat')
    create_time = models.DateTimeField(auto_now_add=True, default=datetime.now())
    author = models.ForeignKey('auth.User', null=False, blank=False)
    chat = models.ForeignKey(Chat, null=False, blank=False)

    def __str__(self):
        return u'{0} {1} {2}'.format(
            self.author.userprofile.get_short_name(), _('for chat'), self.chat.id)