# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Jobs, Questions


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    pass


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['job', 'limit']
    list_filter = ['job__position']
