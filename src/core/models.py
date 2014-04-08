from django.db import models
from django.contrib.auth import get_user_model


class ShareTree(models.Model):
    parent = models.ForeignKey('core.ShareTree', null=True)
    shared_to = models.ForeignKey('auth.User', related_name='shared_to')









