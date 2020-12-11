=============================
Django Lineup
=============================

.. image:: https://badge.fury.io/py/django-lineup.svg
    :target: https://badge.fury.io/py/django-lineup

.. image:: https://travis-ci.org/abidibo/django-lineup.svg?branch=master
    :target: https://travis-ci.org/abidibo/django-lineup

.. image:: https://codecov.io/gh/abidibo/django-lineup/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abidibo/django-lineup

Navigation system for django sites

Documentation
-------------

The full documentation is at https://django-lineup.readthedocs.io.

Quickstart
----------

Install Django Lineup::

    pip install django-lineup

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
