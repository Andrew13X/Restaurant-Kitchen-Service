from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteCookTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="test.user", password="2wsxvfr4", years_of_experience=3
        )

    def test_years_of_experience_in_cook_changelist(self):
        url = reverse("admin:catalog_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_years_of_experience_in_cook_change(self):
        url = reverse("admin:catalog_cook_change", args=[self.cook.id])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_additional_info_fields_in_cook_add(self):
        url = reverse("admin:catalog_cook_add")
        response = self.client.get(url)

        self.assertContains(response, "years_of_experience")
        self.assertContains(response, "Additional info")


class AdminSiteDishTypeTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.admin_user)

    def test_dish_type_is_register_in_admin(self):
        url = reverse("admin:catalog_dishtype_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AdminSiteDishTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.admin_user)

    def test_dish_is_register_in_admin(self):
        url = reverse("admin:catalog_dish_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
