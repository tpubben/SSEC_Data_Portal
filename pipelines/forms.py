import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import CustomUser, Client

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'client_id_fk')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'client_id_fk')


class CustomClientCreationForm(admin.ModelAdmin):

    class Meta:
        model = Client
        fields = ('client_name', 'client_company', 'client_phone', 'client_email')


class CustomClientChangeForm():

    class Meta:
        model = Client
        fields = ('client_name', 'client_company', 'client_phone', 'client_email')