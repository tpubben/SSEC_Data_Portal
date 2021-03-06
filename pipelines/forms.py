from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import *


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
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super(SurveyDateForm, self).__init__(*args, **kwargs)
        self.fields['client_id_fk'].queryset = SurveyDate.objects.filter(client_id_fk=request.user.client_id_fk)


class CreateReportForm(forms.ModelForm):
    class Meta:
        model = SurveyDate
        exclude = ["survey_gas_point_geom","survey_gas_poly_geom", "survey_contour_geom"]
        labels = {
            "client_id_fk": "Client",
            "pipe_id_fk": "Pipeline Name",
            "survey_date": "Date",
            "inf_id_fk": "Site Name",
            "geometry_type": "Site Type",
            "wind_direction": "Wind Direction",
            "flight_duration": "Flight Duration",
            "survey_comments": "Comments",
            "survey_complete": "Survey Complete"
        }
        # widgets = {"survey_gas_point_geom": forms.HiddenInput(), "survey_gas_poly_geom": forms.HiddenInput(), "survey_contour_geom": forms.HiddenInput()}


class LeakForm(forms.ModelForm):
    class Meta:
        model = Deficiency
        fields = "__all__"
        widgets = {"surveydate_id_fk": forms.HiddenInput(), 'deficiency_signoff': forms.HiddenInput(),
                   'deficiency_signoff_date': forms.HiddenInput(), 'deficiency_repaired': forms.HiddenInput()}


class EditLeakForm(forms.ModelForm):
    class Meta:
        model = Deficiency
        fields = ['deficiency_repaired', 'deficiency_signoff', 'deficiency_signoff_date']
        widgets = {'deficiency_signoff': forms.HiddenInput(), 'deficiency_signoff_date': forms.HiddenInput()}




