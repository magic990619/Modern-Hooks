# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ClientGroup(models.Model):
    title = models.CharField(_('Name of company'), max_length=100)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Users of company'), blank=True
    )

    LOGO_POSITION_CHOICES = (
        (1, 'only client logo'),
        (2, 'only right people logo'),
        (3, 'both'),
    )
    logo_position = models.IntegerField(choices=LOGO_POSITION_CHOICES, default=3, blank=True)
    logo = models.ImageField(upload_to='sub_client_group_logos', blank=True, null=True)

    def __str__(self):
        return "Title: {0}".format(self.title)


class SubClientGroup(models.Model):
    client_group = models.ForeignKey('ClientGroup', on_delete=models.CASCADE)
    title = models.CharField(_('Department name'), max_length=100)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Department users'), blank=True
    )

    def __str__(self):
        return "Group: {}, title: {}".format(self.client_group, self.title)
