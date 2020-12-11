#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` templatetags module.
"""

import json
from django.test import TestCase
from lineup.templatetags.lineup_tags import get_all_user_permissions_id_list, set_active_voice
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.template import Context, Template

from lineup.models import MenuItem
from lineup import exceptions


class LineupTagsTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create(
            username='admin',
            password='Passw0rd!uau',
            email='admin@gmail.com',
            is_superuser=True,
        )
        self.user = User.objects.create(
            username='abidibo',
            password='Passw0rd!uau',
            email='abidibo@gmail.com',
        )

        # [(10, 'change_group'), (5, 'add_permission'), (8, 'view_permission'), (24, 'view_session')]
        self.permissions = Permission.objects.filter(id__in=[5, 8, 10, 24])
        self.user.user_permissions.add(self.permissions[0])
        self.user.user_permissions.add(self.permissions[2])

        group = Group.objects.create(name='dev')
        group.permissions.add(self.permissions[1])
        group.permissions.add(self.permissions[3])

        self.user.groups.add(group)

        self.wrong_perm_user = User.objects.create(
            username='wrong',
            password='Passw0rd!uau',
            email='wrong@gmail.com',
        )
        self.wrong_perm_user.user_permissions.add(self.permissions[2])

        self.menu = {
            'label': 'Root',
            'slug': 'main-menu',
            'order': 0,
            'children': [
                {
                    'label': 'Tools',
                    'slug': 'tools',
                    'order': 0,
                    'children': [
                        {
                            'label': 'DNS Tools',
                            'slug': 'dns-tools',
                            'order': 0,
                            'login_required': True,
                            'children': [
                                {
                                    'label': 'DMARC DNS Tools',
                                    'slug': 'dmarc-dns-tools',
                                    'link': '/dmarc-tools/',
                                    'order': 0,
                                }
                            ]
                        },
                        {
                            'label': 'Password Generator',
                            'slug': 'password-generator',
                            'order': 1,
                        }
                    ]
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

    def test_get_all_user_permissions_id_list(self):

        res_ids = sorted(get_all_user_permissions_id_list(self.user))
        expected_ids = sorted([p.id for p in self.permissions])

        self.assertEqual(res_ids, expected_ids)

    def test_from_json_invalid_json(self):
        try:
            invalid_json = "{\"key\" = \"prop\"}"
            MenuItem.from_json(invalid_json)
            self.fail()
        except exceptions.InvalidJson:
            pass

    def test_from_json_unsupported_json_data(self):
        try:
            invalid_json = self.menu.copy()
            MenuItem.from_json(json.dumps([invalid_json, invalid_json]))
            self.fail()
        except exceptions.UnsupportedJsonData:
            pass

    def test_from_json_missing_json_prop(self):
        try:
            invalid_json = self.menu.copy()
            invalid_json.pop('children')
            invalid_json.pop('slug')
            MenuItem.from_json(json.dumps(invalid_json))
            self.fail()
        except exceptions.MissingJsonRequiredProp:
            pass

    def test_from_json(self):
        self.assertEqual(self.tree.children.count(), 3)
        children = self.tree.children.all()
        self.assertEqual(children[0].slug, 'tools')
        self.assertEqual(children[0].children.all()[0].login_required, True)
        self.assertEqual(children[1].enabled, False)
        self.assertEqual(children[2].permissions.all()[0].id, 5)
        self.assertEqual(children[2].permissions.all()[1].id, 24)

    def test_lineup_menu_tag_unexisting_menu(self):
        out = Template(
            "{% load lineup_tags %}"
            "{% lineup_menu 'main-menu_' %}"
        ).render(Context({
            'user': self.user
        }))
        self.assertEqual(out, '\n\n')

    def test_lineup_menu_tag_not_logged_user(self):
        ''' sees just public items '''
        out = Template(
            "{% load lineup_tags %}"
            "{% lineup_menu 'main-menu' %}"
        ).render(Context({
            'user': AnonymousUser()
        }))
        expected = '\n<ul><li><a class="">Tools</a><ul><li><a class="">Password Generator</a></li></ul></li></ul>\n'
        self.assertEqual(out, expected)

    def test_lineup_menu_tag_superuser(self):
        ''' sees all but disabled items '''
        out = Template(
            "{% load lineup_tags %}"
            "{% lineup_menu 'main-menu' %}"
        ).render(Context({
            'user': self.superuser
        }))
        expected = '\n<ul><li><a class="">Tools</a><ul><li><a class="">DNS Tools</a><ul><li><a class="" href="/dmarc-tools/">DMARC DNS Tools</a></li></ul></li><li><a class="">Password Generator</a></li></ul></li><li><a class="">Perm Item</a></li></ul>\n'
        self.assertEqual(out, expected)

    def test_lineup_menu_tag_logged_in_wrong_perms_user(self):
        out = Template(
            "{% load lineup_tags %}"
            "{% lineup_menu 'main-menu' %}"
        ).render(Context({
            'user': self.wrong_perm_user
        }))

        expected = '\n<ul><li><a class="">Tools</a><ul><li><a class="">DNS Tools</a><ul><li><a class="" href="/dmarc-tools/">DMARC DNS Tools</a></li></ul></li><li><a class="">Password Generator</a></li></ul></li></ul>\n'
        self.assertEqual(out, expected)

    def test_lineup_menu_tag_logged_in_user(self):
        out = Template(
            "{% load lineup_tags %}"
            "{% lineup_menu 'main-menu' %}"
        ).render(Context({
            'user': self.user
        }))

        expected = '\n<ul><li><a class="">Tools</a><ul><li><a class="">DNS Tools</a><ul><li><a class="" href="/dmarc-tools/">DMARC DNS Tools</a></li></ul></li><li><a class="">Password Generator</a></li></ul></li><li><a class="">Perm Item</a></li></ul>\n'
        self.assertEqual(out, expected)

    def test_set_active_item(self):
        path = '/dmarc-tools/'
        els = list(self.tree.children.all()[0].children.all()[0].children.all())
        p = MenuItem.objects.get(id=els[0].parent.id)
        self.assertEqual(els[0].active, False)
        self.assertEqual(els[0].parent.with_active, False)
        set_active_voice(path, els)
        self.assertEqual(els[0].active, True)
        self.assertEqual(els[0].parent.with_active, True)
