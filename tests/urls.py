# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, re_path, include
# from django.contrib import admin
from baton.autodiscover import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    re_path(r'^', include('lineup.urls', namespace='lineup')),
]
