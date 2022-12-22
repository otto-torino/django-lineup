# -*- coding: utf-8 -*-
import sys
import json
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from mptt.admin import MPTTModelAdmin

from .models import MenuItem

baton = 'baton' in sys.modules

if baton:
    from baton.admin import RelatedDropdownFilter


class MenuItemInline(admin.StackedInline):
    '''
    Tabular Inline View for MenuItem
    '''
    model = MenuItem
    extra = 1
    classes = ('collapse-entry', 'expand-first', )
    prepopulated_fields = {'slug': ('label',)}


@admin.register(MenuItem)
class MenuItemAdmin(MPTTModelAdmin):
    list_display = ('slug', 'label', 'parent', 'link', 'order', 'login_required', 'enabled', )
    list_filter = (('parent', RelatedDropdownFilter, ) if baton else 'parent', 'enabled', 'login_required', )
    list_editable = ('order', )
    search_fields = ('label', )
    filter_horizontal = ('permissions', )
    inlines = [MenuItemInline, ]
    prepopulated_fields = {'slug': ('label',)}
    fieldsets = (
        (_('Main'), {
            'fields': ('parent', 'label', 'slug', 'link', 'title', 'order', 'extras' ),
            'classes': ('baton-tabs-init', 'baton-tab-fs-permissions', 'baton-tab-inline-children', ),
            'description': _('A menu item without parent identifies a new menu.')

        }),
        (_('Visibility'), {
            'fields': ('enabled', 'login_required', 'permissions', ),
            'classes': ('tab-fs-permissions', ),
            'description': _('Yuo can decide to disable or restrict the visibility of this voice and consequently of all its children. Keep in mind that also if a child is publicly visible, but this voice requires a login, then the child will not be visible to not logged users. The same happens for permissions restrictions.')
        }),
    )

    def baton_cl_rows_attributes(self, request, cl):
        data = {}
        for item in MenuItem.objects.filter(parent__isnull=True):
            data[item.id] = {
                'class': 'table-info',
            }
        return json.dumps(data)
