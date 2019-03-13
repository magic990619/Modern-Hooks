# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Jobs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    position = models.CharField(max_length=255, verbose_name=_('Position'))
    link = models.URLField(_('Interview link'), max_length=500)

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def __str__(self):
        return "{0} {1}".format(self.user.email, self.position)


class Questions(models.Model):
    job = models.ForeignKey('Jobs', verbose_name=_('Job'))
    question = models.TextField(verbose_name=_('Question'))
    limit = models.IntegerField(default=2)
    order = models.IntegerField()
    competency = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
