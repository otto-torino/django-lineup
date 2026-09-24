from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from . import cache
from .models import MenuItem


@method_decorator(staff_member_required, name="dispatch")
class RebuildTreeView(View):
    def post(self, request):
        MenuItem.objects.rebuild()
        # rebuild() uses bulk_update, which does not send post_save signals
        cache.clear()
        return redirect(reverse("admin:lineup_menuitem_changelist"))
