#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` admin module.
"""

import json
from django.test import TestCase, RequestFactory

from django.contrib.admin.sites import AdminSite
from lineup.admin import MenuItemAdmin
from lineup.models import MenuItem


class LineupAdminTest(TestCase):
    """
    Test checking the lineup admin class
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.menu = {
            'label': 'Root',
            'slug': 'main-menu',
            'order': 0,
            'children': [
                {
                    'label': 'Tools',
                    'slug': 'tools',
                    'order': 0,
                },
                {
                    'label': 'Disabled Item',
                    'slug': 'disabled-item',
                    'order': 1,
                    'enabled': False,
                    'children': [
                        {
                            'label': 'Disabled child',
                            'slug': 'disabled-child',
                            'order': 0,
                        }
                    ]
                },
                {
                    'label': 'Perm Item',
                    'slug': 'perm-item',
                    'order': 2,
                    'permissions': ['add_permission', 'view_session']
                }
            ]
        }

        self.tree = MenuItem.from_json(json.dumps(self.menu))

    def test_baton_integration(self):
        request = self.factory.get('/admin/')
        admin = MenuItemAdmin(model=MenuItem, admin_site=AdminSite())
        rows_attributes = admin.baton_cl_rows_attributes(request)

        expected = '{"1": {"class": "table-info"}}'
        self.assertEqual(expected, rows_attributes)
