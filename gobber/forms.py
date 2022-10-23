from django import forms

from django.forms import ModelForm
from gobber.models import AccessKey, Message

class MessageForm(ModelForm):
    
    class Meta:
        model = Message

        # Visible form fields
        fields = ['message_text']
        
        # Customizing textarea
        widgets = {
            'message_text': forms.Textarea(attrs={
                                                    'rows': 5, 
                                                    'style': 'background-color:rgb(139, 137, 134); font-family:PixelFont',
                                                    }),


        }

        # Removing label
        labels = {
            'message_text': '',
        }

class AccessForm(ModelForm):

    class Meta:
        model = AccessKey

        fields = ['key']

        # Hiding user input
        widgets = {
            'key': forms.PasswordInput(),
        }
        
        labels = {
            'key': '',
        }