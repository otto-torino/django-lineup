#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` management commands
"""
import json
import tempfile
import os
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError

from lineup.models import MenuItem


class LineupCommandImportFromJson(TestCase):
    def setUp(self):
        pass

    def test_import_menu_from_json_not_a_file(self):
        try:
            call_command('import_menu_from_json', '/some-unexisting-path/fsjlfhke88ikjgfklnkjlhdskjh.json')
            self.fail()
        except CommandError:
            pass

    def test_import_menu_from_json_empty_json(self):
        f = tempfile.NamedTemporaryFile()
        try:
            call_command('import_menu_from_json', f.name)
            self.fail()
        except CommandError:
            pass

    def test_import_menu_from_json_wrong_json(self):
        f = tempfile.NamedTemporaryFile()
        f.write(b'{"label": "Root", "slug": "imported-menu", "order": 0, children: [{ "label": "Tools", "slug": "tools", "link": "/tools/", "order": 0 }]}')
        f.seek(os.SEEK_SET)
        try:
            call_command('import_menu_from_json', f.name)
            self.fail()
        except CommandError as e:
            self.assertEqual(str(e), 'Cannot import menu: Cannot parse provided json: Expecting property name enclosed in double quotes: line 1 column 56 (char 55)')
            pass

    def test_import_menu_from_json_ok(self):
        self.assertEqual(MenuItem.objects.filter(slug='imported-menu').count(), 0)
        f = tempfile.NamedTemporaryFile()
        f.write(b'{"label": "Root", "slug": "imported-menu", "order": 0, "children": [{ "label": "Tools", "slug": "tools", "link": "/tools/", "order": 0, "extras": {"icon": "fa-user"} }]}')
        f.seek(os.SEEK_SET)
        call_command('import_menu_from_json', f.name)
        self.assertEqual(MenuItem.objects.filter(slug='imported-menu').count(), 1)
        self.assertEqual(MenuItem.objects.filter(slug='tools', parent__slug='imported-menu').count(), 1)
