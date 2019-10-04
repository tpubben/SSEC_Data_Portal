from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'client_id_fk')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    list_display = ['username', 'first_name', 'last_name', 'client_id_fk', 'email',]


class CustomClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_company', 'client_email', 'client_phone']


class CustomClientAdmin(admin.ModelAdmin):
    form = CustomClientForm
    fields = ['client_company', 'client_email', 'client_phone']


class CustomPipelineForm(forms.ModelForm):

    class Meta:
        model = Pipeline
        fields = ['pipe_name', 'client_id_fk', 'pipe_geom']


class CustomPipelineAdmin(admin.ModelAdmin):
    form = CustomPipelineForm
    fields = ['pipe_name', 'client_id_fk', 'pipe_geom']


class CustomSurveyAdmin(admin.ModelAdmin):
    form = SurveyDateForm
    fields = '__all__'



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client, CustomClientAdmin)
admin.site.register(Pipeline, CustomPipelineAdmin)
admin.site.register(SurveyDate)
admin.site.register(Deficiency)
admin.site.register(SurveyPoint)
admin.site.register(Infrastructure)