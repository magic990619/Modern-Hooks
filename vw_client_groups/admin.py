# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from vw_client_groups.forms import SubClientGroupAdminForm
from vw_client_groups.models import ClientGroup, SubClientGroup


@admin.register(SubClientGroup)
class SubClientGroupAdmin(admin.ModelAdmin):
    search_fields = ['client_group', 'title', 'sub_group_users']
    list_display = ('title', 'client_group')
    form = SubClientGroupAdminForm

    def get_queryset(self, request):
        qs = super(SubClientGroupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.client_group:
            return qs.filter(client_group=request.user.client_group)

    def get_form(self, request, *args, **kwargs):
        form = super(SubClientGroupAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        if request.user.client_group:
            form.base_fields['users'].queryset = request.user.client_group.users.all()
        return form

    def has_add_permission(self, request):
        return bool(request.user.client_group)

    def save_model(self, request, obj, form, change):
        obj.client_group = form.current_user.client_group
        obj.save()


admin.site.register(ClientGroup)
