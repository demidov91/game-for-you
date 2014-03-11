from django.utils.translation import ugettext_lazy as _

from django.db import models


class PropertyName(models.Model):
    """
    Record name can be different in different localizations.
    Language is some reference to the localization.
    Records with the same *international_id* mean the same.
    """
    language = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    international_id = models.IntegerField()


class PropertyRecord(models.Model):
    """
    Record of variable type. Record is stored as string, 'view' should render it according to the *type*.
    """
    TEXT_TYPE = 1
    PHONE_NUMBER_TYPE = 2

    DATA_FIELD_CHOICES = (
        (TEXT_TYPE, _('Text type')),
        (PHONE_NUMBER_TYPE, _('Phone number type')),
    )

    name = models.ForeignKey(PropertyName)
    value = models.TextField()
    type = models.PositiveSmallIntegerField(choices=DATA_FIELD_CHOICES)

