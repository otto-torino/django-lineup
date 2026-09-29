#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` admin module.
"""

import json
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import TestCase, RequestFactory
from django.urls import reverse

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
        rows_attributes = admin.baton_cl_rows_attributes(request, None)

        expected = '{"1": {"class": "table-info"}}'
        self.assertEqual(expected, rows_attributes)

    def test_admin_template_does_not_require_mptt_app(self):
        self.assertFalse(apps.is_installed('mptt'))
        get_template('admin/lineup/menuitem/change_list.html')

        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password',
        )
        self.client.force_login(user)
        response = self.client.get(reverse('admin:lineup_menuitem_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_rebuild_tool_is_a_link_that_posts_its_form(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('admin:lineup_menuitem_changelist'))

        url = reverse('lineup:rebuild')
        # a link, which the admin themes style like the other object tools
        self.assertContains(
            response,
            f'<a href="{url}" class="rebuildlink" data-lineup-rebuild-form="lineup-rebuild-form">',
        )
        self.assertContains(
            response,
            f'<form id="lineup-rebuild-form" action="{url}" method="post" hidden>',
        )
        self.assertContains(response, 'lineup/js/rebuild.js')
        self.assertIsNotNone(finders.find('lineup/js/rebuild.js'))
