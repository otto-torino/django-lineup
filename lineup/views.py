from django.urls import reverse
from django.views.generic import View
from django.shortcuts import redirect
from .models import MenuItem

class RebuildTreeView(View):
    def get(self, request):
        MenuItem.objects.rebuild()
        return redirect(reverse('admin:lineup_menuitem_changelist'))
