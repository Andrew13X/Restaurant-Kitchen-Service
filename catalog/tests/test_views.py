from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import DishType, Dish

DISH_TYPE_LIST_URL = reverse("catalog:dish-type-list")
COOK_LIST_URL = reverse("catalog:cook-list")
DISH_LIST_URL = reverse("catalog:dish-list")
PAGINATION = 5


class PublicLoginTest(TestCase):
    def test_dish_type_list_login_required(self):
        response = self.client.get(DISH_TYPE_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_cook_list_login_required(self):
        response = self.client.get(COOK_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_dish_list_login_required(self):
        response = self.client.get(DISH_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_index_page_login_required(self):
        response = self.client.get(reverse("catalog:index"))

        self.assertNotEqual(response.status_code, 200)


class DishTypeListTest(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="Frank",
            password="Test123",
        )
        self.client.force_login(self.cook)
        DishType.objects.create(
            name="<NAME>",
        )
        DishType.objects.create(
            name="<NAME_SECOND>",
        )
        DishType.objects.create(
            name="<NAME_THIRD>",
        )
        DishType.objects.create(
            name="<NAME_FORTH>",
        )
        DishType.objects.create(
            name="<NAME_FIFTH>",
        )
        DishType.objects.create(
            name="<NAME_SIX>",
        )

    def test_retrieve_dish_type_list(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        dish_type_list = DishType.objects.all().order_by("name")
        dish_type_context = response.context["dish_type_list"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/dish_type_list.html")
        self.assertEqual(len(response.context["dish_type_list"]), PAGINATION)
        self.assertEqual(
            list(dish_type_context),
            list(dish_type_list[: len(dish_type_context)]),
        )


class DishListAndDetailTest(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="Bob", password="<PASSWORD>"
        )
        self.client.force_login(self.cook)
        self.dish_type = DishType.objects.create(
            name="<NAME_SECOND>",
        )
        Dish.objects.create(
            name="Napoleon",
            description="Cake",
            price=120.35,
            dish_type=self.dish_type,
        )
        Dish.objects.create(
            name="Karbonara",
            description="Cake",
            price=120.35,
            dish_type=self.dish_type,
        )
        Dish.objects.create(
            name="Bread",
            description="Cake",
            price=120.35,
            dish_type=self.dish_type,
        )

    def test_retrieve_dish_list(self):
        response = self.client.get(DISH_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/dish_list.html")

    def test_retrieve_dish_detail(self):
        response = self.client.get(reverse("catalog:dish-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/dish_detail.html")


class CookListAndDetailTest(TestCase):
    def setUp(self) -> None:
        self.first_cook = get_user_model().objects.create_user(
            username="Bob",
            password="<PASSWORD>",
        )
        get_user_model().objects.create_user(
            username="Ivan",
            password="Test123",
        )
        get_user_model().objects.create_user(
            username="Frank",
            password="Test123",
        )
        self.client.force_login(self.first_cook)

    def test_retrieve_cook_list(self):
        response = self.client.get(COOK_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/cook_list.html")

    def test_retrieve_cook_detail(self):
        response = self.client.get(reverse("catalog:cook-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/cook_detail.html")
