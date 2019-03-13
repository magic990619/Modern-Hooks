# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class VwUserConfig(AppConfig):
    name = 'vw_user'

    def ready(self):
    	import vw_user.signals
