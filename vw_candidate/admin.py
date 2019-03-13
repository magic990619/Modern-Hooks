# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from vw_candidate.models import Candidate, Question, Recording, Rating


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Display the list of Questions
    """
    list_display = ['candidate', 'ques', 'order', 'limit', 'competency']
    fields = ['candidate', 'ques', 'order', 'limit', 'competency']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'rate', 'recording']


admin.site.register(Candidate)
admin.site.register(Recording)
admin.site.register(Rating, RatingAdmin)
