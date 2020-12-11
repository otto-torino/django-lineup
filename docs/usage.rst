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

Add Django Lineup's URL patterns:

.. code-block:: python

    from lineup import urls as lineup_urls


    urlpatterns = [
        ...
        url(r'^', include(lineup_urls)),
        ...
    ]
