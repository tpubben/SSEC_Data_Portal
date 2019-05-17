import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'client_name')


class ClientCreationForm():
    client_company = forms.CharField(help_text='Enter company name.')
    client_email = forms.CharField(help_text='Enter primary contact email.')
    client_phone = forms.CharField(help_text='Enter primary contact phone number.')
