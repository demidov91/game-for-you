from django import forms
from django.utils.translation import ugettext_lazy as _

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


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddTagForm(TagForm):
    class Meta(TagForm.Meta):
        labels = {
            'name': _('New tag name'),
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


class AddCompetitionForm(forms.ModelForm):
    _temp_place_form = PlaceForm()
    _temp_tag_form = AddTagForm()
    _temp_competition_form = CompetitionForm()

    short_place_name = _temp_place_form.fields['name']
    address = _temp_place_form.fields['address']
    new_tag_name = _temp_tag_form.fields['name']
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
        labels = {
            'like_a_place': _('Place created earlier'),
            'new_tag_name': _('New tag name'),
        }

        fields = ('start_datetime', 'name', 'like_a_place', 'short_place_name', 'address', 'tournament',
                  'team_limit', 'team_accept_strategy', 'duration', 'tags', 'new_tag_name')

    checkbox_fields = ('tags',)
    owner = None

    def __init__(self, data=None, owner=None, *args, **kwargs):
        super(AddCompetitionForm, self).__init__(data, *args, **kwargs)
        self.owner = owner
        for none_reuired in ('short_place_name', 'address', 'tags', 'new_tag_name', 'like_a_place'):
            self.fields[none_reuired].required = False

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
        if cleaned_data.get('new_tag_name'):
            additional_tag_id = Tag.objects.create(name=cleaned_data.get('new_tag_name')).id
            tags_id = list(cleaned_data['tags'].values_list('id', flat=True))
            tags_id.append(additional_tag_id)
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

    def save(self, *args, commit=True, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.owners = ShareTree.objects.create(shared_to=self.owner)
        super(AddCompetitionForm, self).save(*args, commit=commit, **kwargs)
