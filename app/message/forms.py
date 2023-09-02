from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control comment-input', 'placeholder': 'Leave a comment here'}))

    class Meta:
        model = Message
        fields = ('content', )