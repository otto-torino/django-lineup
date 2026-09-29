from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View

from . import cache
from .models import MenuItem


@method_decorator(staff_member_required, name="dispatch")
class RebuildTreeView(View):
    def get(self, request):
        """Ask to confirm: a GET must not change the tree.

        The change list posts straight away with its script, so this page is
        seen only without JavaScript.
        """
        context = {
            **admin.site.each_context(request),
            "title": _("Are you sure?"),
            "opts": MenuItem._meta,
        }
        return render(request, "admin/lineup/menuitem/rebuild_confirmation.html", context)

    def post(self, request):
        MenuItem.objects.rebuild()
        # rebuild() uses bulk_update, which does not send post_save signals
        cache.clear()
        return redirect(reverse("admin:lineup_menuitem_changelist"))
