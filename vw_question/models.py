# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class SampleQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=3000)
    type = models.CharField(max_length=50)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)
    competency = models.ForeignKey('Competency', on_delete=models.SET_NULL, null=True, blank=True)
    limit = models.IntegerField(default=2)

    def __str__(self):
        return self.content


class Position(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{0}".format(self.name)


class Competency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name = _('Competency')
        verbose_name_plural = _('Competencies')
