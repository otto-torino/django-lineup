# -*- coding: utf-8 -*-
import hashlib
import uuid

from django.conf import settings
from django.core.cache import cache

VERSION_KEY = "lineup:version"
DEFAULT_TIMEOUT = 600


def get_timeout():
    return getattr(settings, "LINEUP_CACHE_TIMEOUT", DEFAULT_TIMEOUT)


def get_version():
    """
    Returns the current cache version, which is part of every menu key.
    Changing it invalidates all cached menus at once, without deleting
    keys one by one (not every cache backend can list keys).
    """
    version = cache.get(VERSION_KEY)
    if version is None:
        cache.add(VERSION_KEY, uuid.uuid4().hex, None)
        version = cache.get(VERSION_KEY)
    return version


def get_menu_key(slug, user_id, path):
    # hash the path so the key is valid for every backend (e.g. memcached)
    path_hash = hashlib.md5(path.encode("utf-8")).hexdigest()
    return "lineup:%s:%s:%s:%s" % (get_version(), slug, user_id, path_hash)


def get_menu(slug, user_id, path):
    return cache.get(get_menu_key(slug, user_id, path))


def set_menu(slug, user_id, path, value):
    cache.set(get_menu_key(slug, user_id, path), value, get_timeout())


def clear():
    cache.set(VERSION_KEY, uuid.uuid4().hex, None)
