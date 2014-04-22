from django import forms

from tournament.models import Tournament, Competition

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition