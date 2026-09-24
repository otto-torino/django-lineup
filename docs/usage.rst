=====
Usage
=====

To use Django Lineup in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'lineup',
        ...
    )

Add to your main `urls.py`:

.. code-block:: python

    ...
    path("lineup/", include("lineup.urls", namespace="lineup")),
    ...

Be sure the ``requests`` context processor is included (it is by default):

.. code-block:: python

    TEMPLATES = [
      {
        'OPTIONS': {
          'context_processors': [
            # ...
            "django.template.context_processors.request",
          ],
        },
      },
    ]

Caching
-------

Rendered menu trees are cached with Django's default cache, one entry per
menu, user and path. Entries expire after ``LINEUP_CACHE_TIMEOUT`` seconds
(default ``600``; ``None`` never expires):

.. code-block:: python

    LINEUP_CACHE_TIMEOUT = 600

All cached menus are invalidated whenever a menu item is saved or deleted, and
when the tree is rebuilt from the admin.

.. note::

    With a per-process cache (such as the default ``LocMemCache``) and more
    than one worker, invalidation only reaches the worker that handled the
    change, and other workers keep serving the old menu until it expires.
    Use a shared cache backend (Redis, Memcached, database) in production.
