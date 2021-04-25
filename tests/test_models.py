#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_django-lineup
------------

Tests for `django-lineup` models module.
"""

from django.test import TransactionTestCase
from django.db.utils import IntegrityError
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
            extras="icon='fa-cogs'"}
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
                extras="icon='fa-user'"}
            )
            child[i].save()
        order = [c.order for c in primary_nav.children.all()]
        self.assertEqual(list(order), sorted(order))

    def test_creation(self):
        item = models.MenuItem(
            label='Item',
            slug='item',
            link='/item/',
            order=0,
        )
        item.save()
        self.assertEqual(item.id, 1)

    def test_order_required(self):
        item = models.MenuItem(
            label='Item',
            slug='item',
            link='/item/',
        )
        try:
            item.save()
            self.fail()
        except IntegrityError:
            pass

    def test_suplicated_slug(self):
        item = models.MenuItem(
            label='Item',
            slug='item',
            link='/item/',
            order=0
        )
        item.save()

        item2 = models.MenuItem(
            label='Item2',
            slug='item',
            link='/item2/',
            order=1
        )
        item.save()
        try:
            item2.save()
            self.fail()
        except IntegrityError:
            pass
