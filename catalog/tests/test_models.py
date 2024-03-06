from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import DishType, Dish


class ModelTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(
            name="Pasta",
        )

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), f"{self.dish_type.name}")

    def test_dish_str(self):
        dish = Dish.objects.create(
            name="Karbonara",
            description="Karbonara is a pizza",
            price=5.00,
            dish_type=self.dish_type,
        )
        self.assertEqual(str(dish), dish.name)

    def test_create_cook(self):
        username = "Bob123"
        password = "Test123"
        first_name = "Bob"
        last_name = "Bobul"
        years_of_experience = 10
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(
            str(cook), f"{cook.username} ({cook.first_name} {cook.last_name})"
        )
        self.assertEqual(cook.years_of_experience, years_of_experience)
        self.assertTrue(cook.check_password(password))
