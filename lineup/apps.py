# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LineupConfig(AppConfig):
    name = 'lineup'
    verbose_name = _('Menu')
