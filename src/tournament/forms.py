import re

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.utils.encoding import force_text

from tournament.models import Tournament, Competition, PlayField, Tag, TagManagementTree
from core.forms import BootstrapDateTimeField
from core.models import ShareTree
from tournament.utils import create_tags



class PlaceForm(forms.ModelForm):
    class Meta:
        model = PlayField
        fields = ('name', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(PlaceForm, self).clean()
        if not cleaned_data['name'] and not cleaned_data['address']:
            raise forms.ValidationError(_('Enter any data about the place.'))
        return cleaned_data


class AbstractNewTagNamesCleaner:
    tags_separator = re.compile('[,;]\s*')

    def clean_new_tag_names(self):
        if self.cleaned_data['new_tag_names']:
            self.cleaned_data['new_tag_names'] = self.tags_separator.split(self.cleaned_data.get('new_tag_names'))
            if Tag.objects.filter(name__in=self.cleaned_data['new_tag_names']).exists():
                raise forms.ValidationError(u'{0} {1} {2}'.format(_('Tags'), u','.join(Tag.objects.filter(name__in=self.cleaned_data['new_tag_names']).values_list('name', flat=True)),  _(' already exist.')))
        return self.cleaned_data['new_tag_names']

    def clean_and_add_tags(self, cleaned_data):
        """
        Creates new *PlayField* and *Tag* instances if it is necessary.
        """
        if cleaned_data.get('new_tag_names'):
            new_tag_ids = create_tags(cleaned_data.get('new_tag_names'), self.owner)
            tags_id = list(cleaned_data['tags'].values_list('id', flat=True))
            tags_id.extend(new_tag_ids)
            cleaned_data['tags'] = Tag.objects.filter(id__in=tags_id)
        return cleaned_data



class TournamentForm(forms.ModelForm, AbstractNewTagNamesCleaner):
    new_tag_names = forms.CharField(
        label=_('New tag names'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)
    class Meta:
        model = Tournament
        widgets = {
            'first_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'last_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'first_datetime', 'last_datetime', 'tags', 'new_tag_names')

    owner = None

    checkbox_fields = ('tags',)

    def __init__(self, owner, *args, **kwargs):
        """
        owner: *auth.User* instance.
        """
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.owner = owner
        self.fields['tags'].queryset = Tag.objects.filter(
            id__in=TagManagementTree.objects.filter(shared_to=self.owner).values_list('managed__id', flat=True))

    def clean(self):
        return self.clean_and_add_tags(super(TournamentForm, self).clean())

    def save(self, owner, commit=True, *args, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.owner = ShareTree.objects.create(shared_to=owner)
        super(TournamentForm, self).save(*args, commit=commit, **kwargs)


class AddCompetitionForm(forms.ModelForm, AbstractNewTagNamesCleaner):
    _temp_place_form = PlaceForm()

    short_place_name = _temp_place_form.fields['name']
    address = _temp_place_form.fields['address']
    new_tag_names = forms.CharField(
        label=_('New tag names'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)

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
            'place': widgets.Select(attrs={'class': 'form-control'}),
        }

        fields = ('start_datetime', 'name', 'place', 'short_place_name', 'address', 'tournament',
                  'team_limit', 'team_accept_strategy', 'duration', 'tags', 'new_tag_names')

    checkbox_fields = ('tags',)
    owner = None

    #*PlayField* object to use until new *PlayField* instance is created.
    _default_place = PlayField(name='Default place')

    def __init__(self, data=None, owner=None, *args, **kwargs):
        super(AddCompetitionForm, self).__init__(data, *args, **kwargs)
        self.owner = owner
        for none_reuired in ('short_place_name', 'address', 'tags', 'place'):
            self.fields[none_reuired].required = False
        self.fields['place'].queryset = PlayField.objects.filter(owner=owner)
        self.fields['tags'].queryset = Tag.objects.filter(
            id__in=TagManagementTree.objects.filter(shared_to=self.owner).values_list('managed__id', flat=True))

    def clean(self):
        """
        Creates new *PlayField* and *Tag* instances if it is necessary.
        """
        cleaned_data = super(AddCompetitionForm, self).clean()
        if cleaned_data.get('place') == self._default_place and not cleaned_data.get('address') and not cleaned_data.get('short_place_name'):
            self._errors['place'] = [_('Select place where competition is held.')]
            raise forms.ValidationError(_('Select place where competition is held.'))
        if cleaned_data.get('place') == self._default_place:
            self.instance.place = PlayField.objects.create(name=cleaned_data['short_place_name'],
                                                          address=cleaned_data['address'],
                                                          owner=self.owner)
            self.cleaned_data['place'] = self.instance.place
        return self.clean_and_add_tags(cleaned_data)

    def clean_place(self):
        if not self.cleaned_data['place']:
            self.cleaned_data['place'] = self._default_place
        return self.cleaned_data['place']

    def save(self, commit=True, *args, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.owners = ShareTree.objects.create(shared_to=self.owner)
        super(AddCompetitionForm, self).save(*args, commit=commit, **kwargs)

    @transaction.commit_manually
    def is_valid(self):
        if super(AddCompetitionForm, self).is_valid():
            transaction.commit()
            return True
        transaction.rollback()
        return False



class BaseUserPlacesFormset(forms.models.BaseModelFormSet):
    def __init__(self, owner, *args, **kwargs):
        """
        owner: *auth.User* instance.
        """
        super(BaseUserPlacesFormset, self).__init__(*args, **kwargs)
        self.queryset = PlayField.objects.filter(owner=owner)

    def clean(self):
        super(BaseUserPlacesFormset, self).clean()
        cant_delete = False
        for form in self.deleted_forms:
            if Competition.objects.filter(place=form.cleaned_data['id']).exists():
                form._errors['DELETE'] = [_("You can't delete place which has competitions related.")]
                cant_delete = True
        if cant_delete:
            raise forms.ValidationError(_("Can't perform the action."))


UserPlacesFormset = forms.models.modelformset_factory(PlayField,
                                                      formset=BaseUserPlacesFormset,
                                                      form=PlaceForm, can_delete=True)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'has_chat')
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'form-control'})
        }