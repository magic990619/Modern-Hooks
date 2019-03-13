# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from vw_question.models import SampleQuestion, Position, Competency


@admin.register(SampleQuestion)
class SampleQuestionAdmin(admin.ModelAdmin):
    """
    Display the list of SampleQuestion
    """
    list_display = ['position', 'type', 'content', 'competency']
    search_fields = ['position', 'type', 'content', 'competency']
    fields = ['position', 'type', 'content', 'competency']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """
    Display the list of Position
    """
    list_display = ['name', 'user']
    search_fields = ['name']
    fields = ('name', 'user',)


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    """
    Display the list of Competency
    """
    list_display = ['name']
    search_fields = ['name']
    fields = ('name',)
