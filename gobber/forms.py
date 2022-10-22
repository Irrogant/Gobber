from email import message
from pdb import post_mortem
from django import forms

from django.forms import ModelForm
from gobber.models import AccessKey, Message

class MessageForm(ModelForm):
    
    #TODO: clean input?
    class Meta:
        model = Message

        # Visible form fields
        fields = ['message_text']
        
        # Customizing textarea
        widgets = {
            'message_text': forms.Textarea(attrs={'rows': 5,})
        }

        # Removing label
        labels = {
            'message_text': '',
        }

class AccessForm(ModelForm):

    class Meta:
        model = AccessKey

        fields = ['key']

        widgets = {
            'key': forms.PasswordInput(),
        }
        
        labels = {
            'key': '',
        }