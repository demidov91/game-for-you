from django import forms

from chat.models import TagMessage

class TagMessageForm(forms.models.ModelForm):
    class Meta:
        model = TagMessage
        fields = ('text', )
        widgets = {
            'text': forms.widgets.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
            })
        }

    def __init__(self, data=None, owner=None, tag=None, *args, **kwargs):
        super(TagMessageForm, self).__init__(data=data, *args, **kwargs)
        self.owner = owner
        self.tag = tag

    def save(self, *args, **kwargs):
        self.instance.tag = self.tag
        self.instance.author = self.owner
        super(TagMessageForm, self).save(*args, **kwargs)
