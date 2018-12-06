from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', ]
    ordering = ('email', )


admin.site.register(User, CustomUserAdmin)
