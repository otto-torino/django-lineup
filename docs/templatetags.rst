=====
Templatetags
=====

Django Lineup provides 2 templatetags to include the rendered menu and the breadcrumbs in your templates.

Render Lineup Menu
------------------

Templatetag used to render a menu inside a template ::

    {% load lineup_tags %}
    {% lineup_menu 'main-menu' %}

It takes one parameter: the slug of the menu root voice.

Render Lineup Breadcrumbs
------------------

Templatetag used to render the breadcrumbs inside a template ::

    {% load lineup_tags %}
    {% lineup_breadcrumbs 'main-menu' %}

It takes one parameter: the slug of the menu root voice.
