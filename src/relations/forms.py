from django import forms

from relations.models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'members')
