from django import forms
from django.utils.translation import ugettext_lazy as _

from relations.models import Team, UserProfile
from chat.models import Chat

import logging
logger = logging.getLogger(__name__)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'is_draft')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Enter team name'),
                'class': 'form-control',
            }),
        }


class ProfileSettings(forms.ModelForm):
    username = forms.fields.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label=_('nickname'))
    first_name = forms.fields.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=_('first name'))
    last_name = forms.fields.CharField(
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label=_('last name'))

    class Meta:
        model = UserProfile
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'image', 'external_image')
        widgets = {
            'patronymic': forms.widgets.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, instance, *args, **kwargs):
        super(ProfileSettings, self).__init__(instance=instance, *args, **kwargs)
        self.fields['first_name'].initial = instance.user.first_name
        self.fields['last_name'].initial = instance.user.last_name
        self.fields['username'].initial = instance.user.username

    def save(self, commit=True, *args, **kwargs):
        self.instance.user.username = self.cleaned_data.get('username')
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        if not self.cleaned_data.get('image'):
            self.instance.image = UserProfile.DEFAULT_USER_PICK
        if commit:
            self.instance.user.save()
        super(ProfileSettings, self).save(commit=commit, *args, **kwargs)



