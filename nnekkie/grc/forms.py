from django.forms import ModelForm
from django import forms


from .models import GroupChatMessage

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupChatMessage
        fields =['message']
        widgets = {
            'message':forms.TextInput(attrs={'placeholder':'type here', 'class':'p-4 text-black','autofocus':True})
        }