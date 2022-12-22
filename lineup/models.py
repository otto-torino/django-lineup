# -*- coding: utf-8 -*-
import json
import logging
import re

from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.db import transaction

from mptt.models import MPTTModel, TreeForeignKey

from .managers import MenuItemManager
from .exceptions import InvalidJson, UnsupportedJsonData, MissingJsonRequiredProp

logger = logging.getLogger(__name__)


class MenuItem(MPTTModel):
    label = models.CharField(
        _("label"), max_length=50, help_text=_("Display name on the website.")
    )
    slug = models.SlugField(
        _("slug"), unique=True, help_text=_("Unique identifier for the menu voice.")
    )
    parent = TreeForeignKey(
        "self",
        verbose_name=_("parent"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    link = models.CharField(_("link"), max_length=255, blank=True, null=True)
    title = models.CharField(_("title"), max_length=255, blank=True, null=True)
    order = models.IntegerField(_("order"))
    enabled = models.BooleanField(_("enabled"), default=True)
    login_required = models.BooleanField(
        _("login required"),
        default=False,
        help_text=_(
            "If this is checked, only logged-in users will be able to view the item."
        ),  # noqa
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
        help_text=_(
            "If empty, the menu item will be publicly visible, otherwise only users with at least one of the selected permissions could see it."  # noqa
        ),
    )
    extras = models.CharField(
        _("extras"),
        max_length=255,
        blank=True,
        null=True,
        help_text=mark_safe(_("Comma separated list of extra-attributes, e.g.: <code>icon=\"fa fa-user\",data-tooltip=\"Go home!\"</code>")),
    )

    objects = MenuItemManager()

    active = False
    with_active = False

    def __str__(self):
        return "{}".format(self.label)

    class Meta:
        verbose_name = _("Menu item")
        verbose_name_plural = _("Menu items")

    class MPTTMeta:
        order_insertion_by = ("order",)

    @classmethod
    def from_json(cls, json_string):
        try:
            d = json.loads(json_string)
        except Exception as e:
            raise InvalidJson("Cannot parse provided json: %s" % str(e))

        if not isinstance(d, dict):
            raise UnsupportedJsonData(
                "Provided json should be a dictionary containing a single root voice"
            )

        with transaction.atomic():
            res = cls.create_item_from_dict(d)

        return res

    @classmethod
    def create_item_from_dict(cls, d, parent=None):
        if "label" not in d or "slug" not in d or "order" not in d:
            raise MissingJsonRequiredProp(
                "label, slug and order properties are mandatory"
            )

        item = MenuItem.objects.create(
            parent=parent,
            label=d.get("label"),
            slug=d.get("slug"),
            order=d.get("order"),
            link=d.get("link", None),
            title=d.get("title", None),
            enabled=d.get("enabled", True),
            login_required=d.get("login_required", False),
            extras=d.get("extras", None),
        )

        for permission_code in d.get("permissions", []):
            item.permissions.add(Permission.objects.get(codename=permission_code))

        for child in d.get("children", []):
            cls.create_item_from_dict(child, item)

        return item

    def is_active(self, path):
        return self.link and self.link == path

    def extras_dict(self):
        try:
            return dict(
                [re.sub('"|\'', '', i).strip() for i in s.split("=")]
                for s in self.extras.split(",")
            )
        except Exception:
            return {}
