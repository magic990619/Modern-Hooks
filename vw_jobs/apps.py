# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VwJobsConfig(AppConfig):
    name = 'vw_jobs'
    verbose_name = _('Universal Job link')
    verbose_name_plural = _('Universal Job links')

