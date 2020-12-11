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


Example app
---------------------

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Navigate to the root directory of your application (same as `manage.py`)
2. Install the requirements for the package:

		pip install -r requirements_test.txt

3. Make and apply migrations

		python manage.py makemigrations

		python manage.py migrate

4. Run the server

		python manage.py runserver

5. Access from the browser at `http://127.0.0.1:8000`


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
