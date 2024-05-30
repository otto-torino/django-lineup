from django.urls import path

from . import views

app_name = "lineup"
urlpatterns = [
    path("", views.RebuildTreeView.as_view(), name="rebuild"),
]
