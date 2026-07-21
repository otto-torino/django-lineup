from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from lineup.models import MenuItem


class RebuildTreeViewTest(TestCase):
    def setUp(self):
        self.url = reverse("lineup:rebuild")

    def test_anonymous_user_cannot_rebuild_tree_with_get(self):
        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)
        rebuild.assert_not_called()

    def test_anonymous_user_cannot_rebuild_tree_with_post(self):
        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)
        rebuild.assert_not_called()

    def test_non_staff_user_cannot_rebuild_tree(self):
        user = get_user_model().objects.create_user(username="user", password="password")
        self.client.force_login(user)

        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)
        rebuild.assert_not_called()

    def test_staff_user_cannot_rebuild_tree_with_get(self):
        user = get_user_model().objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.client.force_login(user)

        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        rebuild.assert_not_called()

    def test_staff_user_can_rebuild_tree_with_post(self):
        user = get_user_model().objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.client.force_login(user)

        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse("admin:lineup_menuitem_changelist"),
            fetch_redirect_response=False,
        )
        rebuild.assert_called_once_with()

    def test_staff_post_requires_csrf_token(self):
        user = get_user_model().objects.create_user(
            username="staff", password="password", is_staff=True
        )
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)

        with patch.object(MenuItem.objects, "rebuild") as rebuild:
            response = client.post(self.url)

        self.assertEqual(response.status_code, 403)
        rebuild.assert_not_called()
