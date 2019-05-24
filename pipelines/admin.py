from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserChangeForm
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Client

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'client_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    list_display = ['username', 'first_name', 'last_name', 'client_name', 'email',]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)