import re
from chat.models import Chat

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.utils.six import with_metaclass
from django.db.models import SubfieldBase, Q

from ckeditor.widgets import CKEditorWidget

from tournament.models import Tournament, Competition, PlayField, Tag, TagManagementTree, CompetitionOwnersTree,\
    TournamentOwnersTree
from core.forms import BootstrapDateTimeField
from tournament.utils import create_tags, get_managed_tag_ids
from core.utils import string_types

import logging
logger = logging.getLogger(__name__)


TAGS_SEPARATOR = re.compile(',\s*')

class TagNamesField(with_metaclass(SubfieldBase, forms.fields.CharField)):
    def prepare_value(self, value):
        if not value:
            return ''
        if isinstance(value, string_types):
            return value
        return u', '.join(tag.name for tag in Tag.objects.filter(id__in=value))

    def clean(self, value):
        if not value:
            return []
        names = TAGS_SEPARATOR.split(value)
        tags = Tag.objects.filter(name__in=names)
        if tags.count() != len(names):
            for tag in tags:
                names.remove(tag.name)
            raise forms.ValidationError(u'{0} {1} {2}'.format(
                    _('Tags'), u','.join(names), _(' does not exist.')))
        return tags




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
    tags_separator = re.compile(',\s*')

    def clean_new_tag_names(self):
        if self.cleaned_data['new_tag_names']:
            self.cleaned_data['new_tag_names'] = TAGS_SEPARATOR.split(self.cleaned_data.get('new_tag_names'))
            if Tag.objects.filter(name__in=self.cleaned_data['new_tag_names']).exists():
                raise forms.ValidationError(
                    u'{0} {1} {2}'.format(
                        _('Tags'),
                        u','.join(Tag.objects.filter(
                            name__in=self.cleaned_data['new_tag_names']).values_list('name', flat=True)),
                    _(' already exist.')))
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


def get_event_possible_tags(owner, event):
    query = Q(id__in=get_managed_tag_ids(owner))
    if event:
        query |= Q(id__in=event.tags.values_list('id', flat=True))
    return Tag.objects.filter(query)


class TournamentForm(forms.ModelForm, AbstractNewTagNamesCleaner):
    new_tag_names = forms.CharField(
        label=_('New tag names'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)
    tags_request = TagNamesField(
        label=_('Send request for tagging as'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        model = Tournament
        widgets = {
            'first_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'last_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'first_datetime', 'last_datetime', 'description', 'tags', 'tags_request', 'new_tag_names')

    owner = None

    checkbox_fields = ('tags',)

    def __init__(self, owner, *args, **kwargs):
        """
        owner: *auth.User* instance.
        """
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.owner = owner
        self.fields['tags'].queryset = get_event_possible_tags(owner, kwargs.get('instance'))

    def clean(self):
        return self.clean_and_add_tags(super(TournamentForm, self).clean())

    def save(self, commit=True, *args, **kwargs):
        """
        owner: auth.User instance. User, who created this tournament.
        """
        if commit:
            self.instance.chat = Chat.objects.create()
        managed = super(TournamentForm, self).save(commit=commit, *args, **kwargs)
        if commit:
            TournamentOwnersTree.objects.get_or_create(managed=managed, shared_to=self.owner)
        return managed


class AddCompetitionForm(forms.ModelForm, AbstractNewTagNamesCleaner):
    _temp_place_form = PlaceForm()

    short_place_name = _temp_place_form.fields['name']
    address = _temp_place_form.fields['address']
    new_tag_names = forms.CharField(
        label=_('New tag names'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)
    tags_request = TagNamesField(
        label=_('Send request for tagging as'),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        model = Competition
        widgets = {
            'tournament': forms.Select(attrs={'class': 'form-control'}),
            'start_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'end_datetime': BootstrapDateTimeField(attrs={'class': 'form-control'}),
            'team_limit': forms.TextInput(attrs={'class': 'form-control'}),
            'team_accept_strategy': forms.Select(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}, config_name='event'),
            'tags': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'place': widgets.Select(attrs={'class': 'form-control'}),
        }

        fields = ('name', 'start_datetime', 'end_datetime', 'place', 'short_place_name', 'address', 'tournament',
                  'team_limit', 'team_accept_strategy', 'description', 'tags', 'tags_request', 'new_tag_names')

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
        self.fields['tags'].queryset = get_event_possible_tags(owner, kwargs.get('instance'))

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
            self.instance.chat = Chat.objects.create()
        managed = super(AddCompetitionForm, self).save(*args, commit=commit, **kwargs)
        if commit:
            CompetitionOwnersTree.objects.get_or_create(managed=managed, shared_to=self.owner)
        return managed

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
        fields = ('name', 'show_calendar', 'has_chat', 'is_private')
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, *args, **kwargs):
        if commit and self.instance.has_chat and not self.instance.chat:
            chat = Chat()
            chat.save()
            self.instance.chat = chat
        return super(TagForm, self).save(commit=commit, *args, **kwargs)