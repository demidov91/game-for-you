from django import forms
from django.utils.translation import ugettext_lazy as _

from relations.models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'members', 'is_draft')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Enter team name'),
                'class': 'form-control',
            }),
        }
