from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.forms import (
    DishNameSearchForm,
    DishTypeNameSearchForm,
    CookUsernameSearchForm,
)
from catalog.models import Dish, DishType


class DishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            years_of_experience=10,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Pasta",
        )

    def test_create_dish(self):
        response = self.client.post(
            reverse("catalog:dish-create"),
            {
                "name": "Karbonara",
                "description": "Karbonara is a pizza",
                "price": 100,
                "dish_type": self.dish_type.id,
                "cooks": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Dish.objects.get(id=self.user.dishes.first().id).name, "Karbonara"
        )

    def test_update_dish(self):
        dish = Dish.objects.create(
            name="Karbonara",
            description="Italian pasta",
            price=100.25,
            dish_type=self.dish_type,
        )
        response = self.client.post(
            reverse("catalog:dish-update", kwargs={"pk": dish.id}),
            {
                "pk": dish.id,
                "name": "Not Karbonara",
                "description": "Italian pasta",
                "price": 100.25,
                "dish_type": self.dish_type.id,
                "cooks": [self.user.id],
            },
        )
        Dish.objects.get(id=dish.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.get(id=dish.id).name, "Not Karbonara")

    def test_delete_dish(self):
        dish = Dish.objects.create(
            name="Karbonara",
            description="About Karbonara",
            price=100.25,
            dish_type=self.dish_type,
        )
        response = self.client.post(
            reverse("catalog:dish-delete", kwargs={"pk": dish.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=dish.id).exists())


class DishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            years_of_experience=3,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_dish_type(self):
        response = self.client.post(
            reverse(
                "catalog:dish-type-create",
            ),
            {"name": "Karbonara"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.get(id=1).name, "Karbonara")

    def test_update_dish_type(self):
        dish_type = DishType.objects.create(
            name="Pasta",
        )
        response = self.client.post(
            reverse("catalog:dish-type-update", kwargs={"pk": dish_type.id}),
            {"name": "Not Pasta"},
        )
        DishType.objects.get(id=dish_type.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.get(
            id=dish_type.id).name, "Not Pasta")

    def test_delete_dish_type(self):
        dish_type = DishType.objects.create(
            name="Pasta",
        )
        response = self.client.post(
            reverse("catalog:dish-type-delete", kwargs={"pk": dish_type.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(id=dish_type.id).exists())


class CookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            years_of_experience=3,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "Bobby",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Admin",
            "last_name": "User",
            "years_of_experience": 3,
        }

        response = self.client.post(
            reverse("catalog:cook-create"), data=form_data
        )
        new_cook = get_user_model().objects.get(username="Bobby")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_cook.first_name, form_data["first_name"])
        self.assertEqual(new_cook.last_name, form_data["last_name"])
        self.assertEqual(
            new_cook.years_of_experience, form_data["years_of_experience"]
        )
        self.assertTrue(new_cook.check_password("1qazcde3"))

    def test_update_cook_years_of_experience(self):
        cook = get_user_model().objects.create_user(
            username="Bob.user",
            years_of_experience=3,
            password="1qazcde3",
        )
        response = self.client.post(
            reverse("catalog:cook-update", kwargs={"pk": cook.id}),
            {
                "years_of_experience": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=cook.id).years_of_experience, 3
        )

    def test_cook(self):
        cook = get_user_model().objects.create(
            username="Ivan.user",
            first_name="Ivan",
            last_name="Boss",
            password="1qazcde3",
            years_of_experience=3,
        )
        response = self.client.post(
            reverse("catalog:cook-delete", kwargs={"pk": cook.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=cook.id).exists())


class SearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_search_dish_form(self):
        pasta = DishType.objects.create(
            name="Pasta",
        )
        cakes = DishType.objects.create(
            name="Cakes",
        )
        Dish.objects.create(
            name="Karbonara",
            description="Italian pasta",
            price=100.25,
            dish_type=pasta,
        )
        Dish.objects.create(
            name="Napoleon",
            description="Cake",
            price=120.35,
            dish_type=cakes,
        )
        form = DishNameSearchForm(data={"name": "Karbonara"})
        form.is_valid()
        self.assertEqual(
            list(
                Dish.objects.filter(
                    name__icontains=form.cleaned_data.get("name")
                )
            ),
            list(Dish.objects.filter(name__icontains="Karbonara")),
        )

    def test_search_dish_type_form(self):
        DishType.objects.create(
            name="Pasta",
        )
        DishType.objects.create(
            name="Cakes",
        )
        form = DishTypeNameSearchForm(data={"name": "Pasta"})
        form.is_valid()
        self.assertEqual(
            list(
                DishType.objects.filter(
                    name__icontains=form.cleaned_data.get("name")
                )
            ),
            list(DishType.objects.filter(name__icontains="Pasta")),
        )

    def test_search_cook_form(self):
        get_user_model().objects.create_user(
            username="Frank12",
            first_name="Frank",
            last_name="Franklyn",
            password="1qazcde3",
            years_of_experience=3,
        )
        get_user_model().objects.create_user(
            username="David123",
            first_name="David",
            last_name="Danya",
            password="1qazcde3",
            years_of_experience=3,
        )
        form = CookUsernameSearchForm(data={"username": "David123"})
        form.is_valid()
        self.assertEqual(
            list(
                get_user_model().objects.filter(
                    username__icontains=form.cleaned_data.get("username")
                )
            ),
            list(
                get_user_model().objects.filter(username__icontains="David123")
            ),
        )
