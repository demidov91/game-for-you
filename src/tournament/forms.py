import re

from django import forms
from django.forms import widgets
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from tournament.models import Tournament, Competition, PlayField, Tag
from core.forms import BootstrapDateTimeField
from core.models import ShareTree



class PlaceForm(forms.ModelForm):
    class Meta:
        model = PlayField
        fields = ('name', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        widgets = {
            'first_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'last_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'first_datetime', 'last_datetime', 'tags')

    checkbox_fields = ('tags',)

    def save(self, owner, commit=True, *args, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.owner = ShareTree.objects.create(shared_to=owner)
        super(TournamentForm, self).save(*args, commit=commit, **kwargs)


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        widgets = {
            'place': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'place': _('Place created earlier'),
        }


class AddCompetitionForm(forms.ModelForm):
    _temp_place_form = PlaceForm()
    _temp_competition_form = CompetitionForm()
    tags_separator = re.compile('[,;]\s*')

    short_place_name = _temp_place_form.fields['name']
    address = _temp_place_form.fields['address']
    new_tag_names = forms.CharField(label=_('New tag names'), widget=widgets.TextInput(attrs={'class': 'form-control'}))
    like_a_place = _temp_competition_form.fields['place']

    class Meta:
        model = Competition
        widgets = {
            'tournament': forms.Select(attrs={'class': 'form-control'}),
            'start_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'team_limit': forms.TextInput(attrs={'class': 'form-control'}),
            'team_accept_strategy': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        fields = ('start_datetime', 'name', 'like_a_place', 'short_place_name', 'address', 'tournament',
                  'team_limit', 'team_accept_strategy', 'duration', 'tags', 'new_tag_names')

    checkbox_fields = ('tags',)
    owner = None

    def __init__(self, data=None, owner=None, *args, **kwargs):
        super(AddCompetitionForm, self).__init__(data, *args, **kwargs)
        self.owner = owner
        for none_reuired in ('short_place_name', 'address', 'tags', 'like_a_place'):
            self.fields[none_reuired].required = False

    @transaction.commit_on_success
    def clean(self):
        """
        Creates new *PlayField* and *Tag* instances if it is necessary.
        """
        cleaned_data = super(AddCompetitionForm, self).clean()
        if not cleaned_data.get('like_a_place') and not cleaned_data.get('address') and not cleaned_data.get('short_place_name'):
            self._errors['like_a_place'] = [_('Select place where competition is held.')]
            raise forms.ValidationError(_('Select place where competition is held.'))
        if not cleaned_data.get('like_a_place'):
            self.instance.place = PlayField.objects.create(name=cleaned_data['short_place_name'],
                                                          address=cleaned_data['address'],
                                                          owner=self.owner)
        if cleaned_data.get('new_tag_names'):
            new_tag_ids = tuple(Tag.objects.create(name=name,
                                 first_owners=ShareTree.objects.create(shared_to=self.owner),
                                 first_sharers=ShareTree.objects.create(shared_to=self.owner)).id for name in self.tags_separator.split(cleaned_data.get('new_tag_names')))

            tags_id = list(cleaned_data['tags'].values_list('id', flat=True))
            tags_id.extend(new_tag_ids)
            cleaned_data['tags'] = Tag.objects.filter(id__in=tags_id)
        return cleaned_data

    def clean_new_tag_name(self):
        if self.cleaned_data['new_tag_name'] and Tag.objects.filter(name=self.cleaned_data['new_tag_name']).exists():
            raise forms.ValidationError(_('Tag ') + self.cleaned_data['new_tag_name'] + _(' already exists.'))
        return self.cleaned_data['new_tag_name']


    def clean_like_a_place(self):
        if self.cleaned_data['like_a_place']:
            self.instance.place = self.cleaned_data['like_a_place']
        return self.cleaned_data['like_a_place']

    def save(self, commit=True, *args, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.owners = ShareTree.objects.create(shared_to=self.owner)
        super(AddCompetitionForm, self).save(*args, commit=commit, **kwargs)
