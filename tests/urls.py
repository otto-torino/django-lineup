# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView
from django.urls import path, re_path, include
# from django.contrib import admin
from baton.autodiscover import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
]
