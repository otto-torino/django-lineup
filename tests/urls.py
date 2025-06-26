# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
# from django.contrib import admin
from baton.autodiscover import admin

urlpatterns = [
    path('baton/', include('baton.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    path('lineup/', include('lineup.urls')),
]

# urlpatterns += i18n_patterns(
#     path('baton/', include('baton.urls')),
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='home.html'), name='home'),
#     path('lineup/', include('lineup.urls')),
# )
