from email import message
from pdb import post_mortem
from django import forms

from django.forms import ModelForm
from gobber.models import Message

class MessageForm(ModelForm):
    #Making the input field larger
    # message_text = forms.CharField(label='')
    # message_text = forms.CharField(widget=forms.Textarea, label='')
    
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

    



# class ChatForm(forms.Form):
#     chat = forms.CharField(label='Enter a message', max_length=200)

#     def clean_chat(self):
#         cleanChat = self.cleaned_data['chat']
#         return cleanChat
    
