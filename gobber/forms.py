from email import message
from pdb import post_mortem
from django import forms

from django.forms import ModelForm
from gobber.models import AccessKey, Message

class MessageForm(ModelForm):
    #Making the input field larger
    # message_text = forms.CharField(label='')
    # message_text = forms.CharField(widget=forms.Textarea, label='')
    
    #TODO: clean input?
    class Meta:
        model = Message

        #The form fields we want to be visible
        fields = ['message_text']
        
        #Customizing textarea
        widgets = {
            'message_text': forms.Textarea(attrs={
                                                    'rows': 5,
                                                    })
        }

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