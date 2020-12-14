=====
Usage
=====

To use Django Lineup in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'lineup.apps.LineupConfig',
        ...
    )

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
