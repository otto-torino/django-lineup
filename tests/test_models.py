#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` models module.
"""

from django.test import TransactionTestCase
from lineup import models


class TreeOrder(TransactionTestCase):
    """
    Test checking that if children added out of order to a new tree will be
    ordered properly when called.
    The original source of this bug is django-mptt but this does check that menu
    item is ordering by the correct attributes as well.
    https://github.com/django-mptt/django-mptt/issues#issue/14
    """
    def test_order(self):
        primary_nav = models.MenuItem(
            label='primary-nav',
            slug='primary-nav',
            order=0,
        )
        primary_nav.save()
        child = {}
        for i in [2, 4, 5, 1, 0, 8]:
            child[i] = models.MenuItem(
                parent=primary_nav,
                label=str(i),
                slug=str(i),
                order=i,
                link='/',
            )
            child[i].save()
        order = models.MenuItem.objects.exclude(
            slug='primary-nav').values_list('order', flat=True)
        self.assertEqual(list(order), sorted(order))
