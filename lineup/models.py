# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class MenuItem(MPTTModel):
    label = models.CharField(_('label'),
                             max_length=50,
                             help_text=_('Display name on the website.'))
    slug = models.SlugField(
        _('slug'),
        unique=True,
        help_text=_('Unique identifier for the menu voice.'))
    parent = TreeForeignKey('self',
                            verbose_name=_('parent'),
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children')
    link = models.CharField(_('link'), max_length=255, blank=True, null=True)
    order = models.IntegerField(_('order'))
    enabled = models.BooleanField(_('enabled'))
    login_required = models.BooleanField(
        _('login required'),
        default=False,
        help_text=_(
            'If this is checked, only logged-in users will be able to view the page.'
        )  # noqa
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
        help_text=_(
            'If empty, the menu item will be publicly visible, otherwise only users with at least one of the selected permissions could see it.'
        )  # noqa
    )

    def __str__(self):
        return '{}'.format(self.label)

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

    class MPTTMeta:
        order_insertion_by = ('order', )
