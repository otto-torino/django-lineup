# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LineupConfig(AppConfig):
    # Keep the primary key type in sync with the historical migration even
    # when the host project defaults to BigAutoField.
    default_auto_field = 'django.db.models.AutoField'
    name = 'lineup'
    verbose_name = _('Menu')
