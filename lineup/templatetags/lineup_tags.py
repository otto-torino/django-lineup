# -*- coding: utf-8 -*-
import logging

from django import template
from django.contrib.auth.models import Permission
from django.db.models import Q

from ..models import MenuItem

register = template.Library()
logger = logging.getLogger(__name__)


def get_all_user_permissions_id_list(user):
    # individual permissions
    perms = list(
        Permission.objects.filter(user=user).values_list('id', flat=True)
    )
    # permissions that the user has via a group
    group_perms = list(
        Permission.objects.filter(group__user=user).values_list('id', flat=True)
    )
    return perms + group_perms


@register.inclusion_tag('lineup/menu.html', takes_context=True)
def lineup_menu(context, slug, css=None):
    '''
    Renders one tree level given the slug of the parent node.
    When called recursively can render the whole tree.
    '''
    EMPTY = {'items': None}

    try:
        root = MenuItem.objects.get(slug=slug)
    except MenuItem.DoesNotExist:
        logger.error('Provided lineup menu slug %s not found' % slug)
        return EMPTY

    # get current user
    user = context.get('user')

    # if root is not enabled, do not show children
    if not root.enabled:
        return EMPTY

    # if root visibility restrictions and user is not authenticated do not show children
    if not user.is_authenticated and (root.login_required or root.permissions.count()):  # noqa
        return EMPTY

    if not user.is_authenticated:
        # unlogged user sees only public items
        items = root.children.enabled(login_required=False, permissions=None)
    elif user.is_superuser:
        # superuser sees all enabled items
        items = root.children.enabled()
    else:
        # logged in user which is not superuse should check for permissions
        permissions = context.get('permissions', None)
        if permissions is None:
            permissions = get_all_user_permissions_id_list(user)
            # put in context to avoid querying again at every iteration
            context['permissions'] = permissions

        items = root.children.enabled(
            Q(permissions__id__in=permissions) | Q(permissions=None)
        ).distinct()

    context['items'] = items
    context['css'] = css

    return context
