# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import InviteTemplate, CustomizedUser


@admin.register(CustomizedUser)
class CustomUserAdmin(UserAdmin):
    model = CustomizedUser
    empty_value_display = 'unknown'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('client_group',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'username', 'client_group', 'is_active', 'is_superuser',)
    list_display_links = ('email', 'username', 'client_group', 'is_active', 'is_superuser',)


admin.site.register(InviteTemplate)
