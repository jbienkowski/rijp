# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RijpPortalConfig(AppConfig):
    name = 'rijp_portal'

    def ready(self):
        from . import signals
