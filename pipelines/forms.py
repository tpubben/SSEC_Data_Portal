import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import CustomUser, Client, Pipeline, SurveyDate

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

'''
class PipelineDateForm(forms.ModelForm):
    class Meta:
        model = SurveyDate
        fields = ('pipe_id_fk',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pipe_id_fk'].queryset = Pipeline.objects.none()
'''