# -*- coding: utf-8 -*-
import logging
from django.core.cache import cache

from django import template
from django.contrib.auth.models import Permission
from django.db.models import Q, Count
from django.urls import LocalePrefixPattern

from ..models import MenuItem

register = template.Library()
logger = logging.getLogger(__name__)


def get_all_user_permissions_id_list(user):
    """
    Returns a flat list of all user permissions ids
    """
    # individual permissions
    perms = list(Permission.objects.filter(user=user).values_list("id", flat=True))
    # permissions that the user has via a group
    group_perms = list(
        Permission.objects.filter(group__user=user).values_list("id", flat=True)
    )
    return perms + group_perms


def remove_prefix(text, prefix): # TODO: introduce in python 3.9, so this can be removed
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def set_active_voice(path, items):
    """
    Sets the active property to the active voice, and with_active to
    all its parents
    """

    l = LocalePrefixPattern(prefix_default_language=True)
    prefix = l.language_prefix
    for item in items:
        if item.get("instance").is_active(remove_prefix(path, prefix)):
            item["active"] = True
            parent = item.get("parent")
            while parent is not None:
                parent["has_active"] = True
                parent = parent.get("parent")


def create_tree(context, root, parent=None):
    # get current user
    user = context.get("user")

    # if root is not enabled, do not show children
    if not root.enabled:
        return {}

    # if root visibility restrictions and user is not authenticated do not show children
    if not user.is_authenticated and (
        root.login_required or root.permissions_count > 0
    ):  # noqa
        return {}

    if not user.is_authenticated:
        # unlogged user sees only public items
        items = root.children.enabled(login_required=False, permissions=None).annotate(permissions_count=Count("permissions"))
    elif user.is_superuser:
        # superuser sees all enabled items
        items = root.children.enabled().annotate(permissions_count=Count("permissions"))
    else:
        # logged in user which is not superuse should check for permissions
        permissions = context.get("lineup_permissions", None)
        if permissions is None:
            permissions = get_all_user_permissions_id_list(user)
            # put in context to avoid querying again at every iteration
            context["lineup_permissions"] = permissions

        items = root.children.enabled(
            Q(permissions__id__in=permissions) | Q(permissions=None)
        ).annotate(permissions_count=Count("permissions")).distinct()

    # parent needed to traverse upward for has-active functionality
    el = {"instance": root, "parent": parent}
    el["children"] = [create_tree(context, child, el) for child in items]

    # search active voice
    if "request" in context:
        path = context["request"].META["PATH_INFO"]
        set_active_voice(path, el["children"])

    return el


@register.inclusion_tag("lineup/menu.html", takes_context=True)
def lineup_menu(context, item):
    """
    Renders the whole tree if called recursively with different item param.
    - If item is a slug, the whole tree dictionary is created. and the first
    level items rendered.
    - If item is a dict, it just continues traversing rendering its children.
    """
    if isinstance(item, str):
        try:
            # cache depends on user (permissions) and path (active item)
            path = ""
            user = context.get("user")
            if "request" in context:
                path = context["request"].META["PATH_INFO"]
            t = cache.get_or_set("lineup", {}, None)
            key = "%s:%s" % (user.id, path)
            if t.get(key, None) is None:
                root = MenuItem.objects.prefetch_related("children", "permissions").annotate(permissions_count=Count("permissions")).get(slug=item)
                tree = create_tree(context, root)
                items = tree.get("children", [])
                slug = item
                level = root.level
                t[key] = (items, slug, level)
                cache.set("lineup", t, None)
            else:
                (items, slug, level) = t[key]
        except MenuItem.DoesNotExist:
            logger.error("Provided lineup menu slug %s not found" % item)
            return context
    elif isinstance(item, dict):
        items = item.get("children")
        slug = item.get("instance").slug
        level = item.get("instance").level

    else:
        items = []
        slug = None
        level = None

    context["items"] = items
    context["slug"] = slug
    context["level"] = level

    return context


@register.inclusion_tag("lineup/breadcrumbs.html", takes_context=True)
def lineup_breadcrumbs(context, slug):
    """
    Renders menu breadcrumbs.
    """
    if "request" in context:
        path = context["request"].META["PATH_INFO"]
        active_items = MenuItem.objects.enabled(link=path)

        found = False
        items = []
        for active_item in active_items:
            items.append(active_item)
            parent = active_item.parent
            while parent is not None and parent.enabled:
                items.insert(0, parent)
                parent = parent.parent
            if items.pop(0).slug == slug:
                found = True
                break

        if found:
            context["items"] = items
        else:
            context["items"] = []
    return context
