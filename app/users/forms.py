

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'phone', 'email')

        # help_texts = {
        #     'username': _('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        #     'email': _('Required. Please use a valid email address'),
        #     'password1': _('Your password must contain at least 8 characters.'),
        #     'password2': _('Enter the same password as before, for verification.')
        # }

    email = forms.EmailField()
    phone = forms.CharField(required=False,)


class CustomForm(forms.Form):

    username = forms.CharField(label='Username', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))









