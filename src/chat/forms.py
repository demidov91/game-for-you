from django import forms

from chat.models import Message

class MessageForm(forms.models.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )
        widgets = {
            'text': forms.widgets.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
            })
        }

    def __init__(self, data=None, owner=None, chat=None, *args, **kwargs):
        super(MessageForm, self).__init__(data=data, *args, **kwargs)
        self.owner = owner
        self.chat = chat

    def save(self, *args, **kwargs):
        self.instance.chat = self.chat
        self.instance.author = self.owner
        super(MessageForm, self).save(*args, **kwargs)
