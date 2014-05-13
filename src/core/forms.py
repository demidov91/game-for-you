from django.utils.safestring import mark_safe

from django.forms.widgets import DateTimeInput


class BootstrapDateTimeField(DateTimeInput):
    def render(self, name, value, attrs=None):
        return mark_safe('<div class="datetimepicker" data-date-format="DD.MM.YYYY HH:mm">{0}<span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div>'.format(
            super(BootstrapDateTimeField, self).render(name, value, attrs)
        ))
