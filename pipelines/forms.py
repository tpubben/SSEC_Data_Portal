import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import CustomUser, Client, SurveyDate

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


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


class SurveyDateForm(forms.ModelForm):
    class Meta:
        model = SurveyDate
        fields = ['client_id_fk', 'pipe_id_fk', 'survey_date']

    def __init__(self, request, *args, **kwargs):
        super(SurveyDateForm,self).__init__(*args, **kwargs)
        self.fields['client_id_fk'].queryset = SurveyDate.objects.filter(client_id_fk=request.user.client_id_fk)

