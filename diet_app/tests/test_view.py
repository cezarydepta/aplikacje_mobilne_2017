from django.db import IntegrityError, transaction
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient

from diet_app.models import *


class DiaryViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)

    def test_diary_get_correct_params(self):
        """Testing GET diary view with correct params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id, 'date': self.date})
        assert response.status_code == 200
        assert response.json() == {'diary_id': self.diary.id}

    def test_diary_post_correct_params(self):
        """Testing POST diary view with correct params"""
        # Test creating already existing Diary
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': self.date})
        assert response.status_code == 200
        assert response.json() == {'diary_id': self.diary.id}

        # Test creating not existing Diary
        count = Diary.objects.all().count()
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': '2020-12-12'})
        assert response.status_code == 200
        assert count + 1 == Diary.objects.all().count()

    def test_diary_get_missing_params(self):
        """Testing GET diary view with missing params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id})
        assert response.status_code == 400
        assert response.json() == {'date': ['This field is required.']}

        response = self.client.get(reverse('diary'), {'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}

        response = self.client.get(reverse('diary'), {})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.'], 'date': ['This field is required.']}

    def test_diary_post_missing_params(self):
        """Testing POST diary view with missing params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id})
        assert response.status_code == 400
        assert response.json() == {'date': ['This field is required.']}

        response = self.client.post(reverse('diary'), {'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}

        response = self.client.post(reverse('diary'), {})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.'], 'date': ['This field is required.']}

    def test_diary_get_incorrect_params(self):
        """Testing GET diary view with incorrect params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'date': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].']}

    def test_diary_post_incorrect_params(self):
        """Testing POST diary view with incorrect params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'date': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].']}


class DisciplineViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.discipline = Discipline.objects.create(name='Bieganie', calories_burn=400)

    def test_discipline_get_correct_params(self):
        """Testing GET discipline view with correct params"""
        response = self.client.get(reverse('discipline'), {'id': self.discipline.id})
        assert response.status_code == 200
        assert response.json() == {'name': self.discipline.name, 'calories_burn': self.discipline.calories_burn}

    def test_discipline_get_incorrect_params(self):
        """Testing GET discipline view with incorrect params"""
        response = self.client.get(reverse('discipline'), {'id': 'Majestic Unicorn'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_discipline_get_missing_params(self):
        """Testing GET discipline view with missing params"""
        response = self.client.get(reverse('discipline'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}


class DisciplinesViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.discipline1 = Discipline.objects.create(name='Bieganie', calories_burn=400)
        self.discipline2 = Discipline.objects.create(name='Taniec', calories_burn=300)

    def test_disciplines_get_correct_params(self):
        """Testing GET disciplines view with correct params"""
        response = self.client.get(reverse('disciplines'), {'name': 'ga'})
        assert response.status_code == 200
        assert response.json() == [{'id': self.discipline1.id,
                                    'name': self.discipline1.name,
                                    'calories_burn': self.discipline1.calories_burn}]

        response = self.client.get(reverse('disciplines'), {'name': 'a'})
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': self.discipline1.id,
                'name': self.discipline1.name,
                'calories_burn': self.discipline1.calories_burn
            },
            {
                'id': self.discipline2.id,
                'name': self.discipline2.name,
                'calories_burn': self.discipline2.calories_burn
            }]

        response = self.client.get(reverse('disciplines'), {'name': 'Dancing with unicorns'})
        assert response.status_code == 200
        assert response.json() == []

        response = self.client.get(reverse('disciplines'), {'name': ''})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field may not be blank.']}

    def test_disciplines_get_missing_params(self):
        """Testing GET disciplines view with missing params"""
        response = self.client.get(reverse('disciplines'), {})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field is required.']}


class ActivityViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date1 = "2017-12-13"
        self.date2 = "2017-12-14"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary1 = Diary.objects.create(user=self.user, date=self.date1)
        self.diary2 = Diary.objects.create(user=self.user, date=self.date2)
        self.discipline1 = Discipline.objects.create(name='Dancing with unicorns', calories_burn=500)
        self.discipline2 = Discipline.objects.create(name='Running with unicorns', calories_burn=600)
        self.activity1 = Activity.objects.create(diary=self.diary1, discipline=self.discipline1, time='00:30:00')
        self.activity2 = Activity.objects.create(diary=self.diary1, discipline=self.discipline2, time='00:40:00')
        self.activity3 = Activity.objects.create(diary=self.diary2, discipline=self.discipline1, time='00:35:00')

    def test_activity_get_correct_params(self):
        """Testing GET activity view with correct params"""
        response = self.client.get(reverse('activity'), {'id': self.activity1.id})
        assert response.status_code == 200
        assert response.json() == {'name': self.activity1.discipline.name,
                                   'calories_burn': self.activity1.discipline.calories_burn,
                                   'time': self.activity1.time}

    def test_activity_get_incorrect_params(self):
        """Testing GET activity view with incorrect params"""
        response = self.client.get(reverse('activity'), {'id': 'pozdro600'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_activity_get_missing_params(self):
        """Testing GET activity view with missing params"""
        response = self.client.get(reverse('activity'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}

    def test_activity_post_correct_params(self):
        """Testing POST activity view with correct params"""
        activities_before = Activity.objects.all().count()
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline1.id,
                'time': '00:20:00'
            }
        )
        activities_after = Activity.objects.all().count()

        assert response.status_code == 200
        assert response.json() == {}
        assert activities_before + 1 == activities_after

    def test_activity_post_incorrect_params(self):
        """Testing POST activity view with incorrect params"""
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline2.id,
                'time': '00200:00'
            }
        )

        assert response.status_code == 400
        assert response.json() == {
            'time': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].']
        }

    def test_activity_post_missing_params(self):
        """Testing POST activity view with missing params"""
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline2.id
            }
        )
        assert response.status_code == 400
        assert response.json() == {'time': ['This field is required.']}

    def test_activity_delete_correct_params(self):
        """Testing DELETE activity view with correct params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {'id': self.activity1.id})
        activities_after = Activity.objects.all().count()
        assert response.status_code == 200
        assert response.json() == {}
        assert activities_before - 1 == activities_after

    def test_activity_delete_incorrect_params(self):
        """Testing DELETE activity view with incorrect params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {'id': 'lama'})
        activities_after = Activity.objects.all().count()

        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert activities_before == activities_after

    def test_activity_delete_missing_params(self):
        """Testing DELETE activity view with missing params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {})
        activities_after = Activity.objects.all().count()

        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert activities_before == activities_after


class ProductViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.name = 'Kanapeckzi'
        self.kcal = 300
        self.carbs = 15
        self.proteins = 5
        self.fat = 5

    def test_product_get_correct_params(self):
        """Testing GET product view with correct params"""
        response = self.client.get(reverse('product'), {'id': self.product1.id})
        assert response.status_code == 200
        assert response.json() == {'name': self.product1.name,
                                   'kcal': self.product1.kcal,
                                   'carbs': self.product1.carbs,
                                   'proteins': self.product1.proteins,
                                   'fat': self.product1.fat}

    def test_product_get_incorrect_params(self):
        """Testing GET product view with incorrect params"""
        response = self.client.get(reverse('product'), {'id': 'krzeslo'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_product_get_missing_params(self):
        """Testing GET product view with missing params"""
        response = self.client.get(reverse('product'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}

    def test_product_post_correct_params(self):
        """Testing POST product view with correct params"""
        response = self.client.post(
            reverse('product'), {'name': self.name,
                                 'kcal': self.kcal,
                                 'carbs': self.carbs,
                                 'proteins': self.proteins,
                                 'fat': self.fat}
        )
        new_product = Product.objects.filter(name=self.name).get()
        assert response.status_code == 200
        assert response.json() == {'product_id': new_product.id}

    def test_product_post_incorrect_params(self):
        """Testing POST product view with incorrect params"""
        response = self.client.post(
            reverse('product'), {'name': 'Makaronik',
                                 'kcal': 'drzewo',
                                 'carbs': self.carbs,
                                 'proteins': self.proteins,
                                 'fat': self.fat}
        )
        assert response.status_code == 400
        assert response.json() == {'kcal': ['A valid number is required.']}

    def test_product_post_missing_params(self):
        """Testing POST product view with missing params"""
        response = self.client.post(reverse('product'), {})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field is required.'],
                                   'kcal': ['This field is required.'],
                                   'carbs': ['This field is required.'],
                                   'proteins': ['This field is required.'],
                                   'fat': ['This field is required.']}


class ProductsViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.name = 'Kanapeckzi'
        self.kcal = 300
        self.carbs = 15
        self.proteins = 5
        self.fat = 5

    def test_products_get_correct_params(self):
        """Testing GET products view with correct params"""
        response = self.client.get(reverse('products'), {'name': 'k'})
        assert response.status_code == 200
        assert response.json() == [
            {
                'product_id': self.product1.id,
                'name': self.product1.name
            },
            {
                'product_id': self.product2.id,
                'name': self.product2.name
            }
        ]

        response = self.client.get(reverse('products'), {'name': 'kasza'})
        assert response.status_code == 200
        assert response.json() == [
            {
                'product_id': self.product1.id,
                'name': self.product1.name
            }
        ]

    def test_products_get_missing_params(self):
        """Testing GET products view with missing params"""
        response = self.client.get(reverse('products'), {})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field is required.']}


class IngredientViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)
        self.meal_type = MealType.objects.create(diary=self.diary, name='Śniadanko')
        self.meal = Meal.objects.create(meal_type=self.meal_type)
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.ingredient = Ingredient.objects.create(meal=self.meal, product=self.product1, amount=2.2)

    def test_ingredient_post_correct_params(self):
        """Testing POST ingredient view with correct params"""
        count = Ingredient.objects.all().count()
        response = self.client.post(reverse('ingredient'), {'product_id': self.product1.id,
                                                            'meal_id': self.meal.id,
                                                            'amount': 3})
        new_ingredient = Ingredient.objects.get(id=2)
        assert response.status_code == 200
        assert count == Ingredient.objects.all().count() - 1
        assert response.json() == {'ingredient_id': new_ingredient.id}

    def test_ingredient_post_incorrect_params(self):
        """Testing POST ingredient view with incorrect params"""
        response = self.client.post(reverse('ingredient'), {'product_id': self.product1.id,
                                                            'meal_id': self.meal.id,
                                                            'amount': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'amount': ['A valid number is required.']}

    def test_ingredient_post_missing_params(self):
        """Testing POST ingredient view with missing params"""
        response = self.client.post(reverse('ingredient'), {'product_id': self.product1.id,
                                                            'amount': 3})
        assert response.status_code == 400
        assert response.json() == {'meal_id': ['This field is required.']}

    def test_ingredient_delete_correct_params(self):
        """Testing DELETE ingredient view with correct params"""
        count = Ingredient.objects.all().count()
        response = self.client.delete(reverse('ingredient'), {'id': self.ingredient.id})
        assert response.status_code == 200
        assert response.json() == {}
        assert count == Ingredient.objects.all().count() + 1

    def test_ingredient_delete_incorrect_params(self):
        """Testing DELETE ingredient view with incorrect params"""
        count = Ingredient.objects.all().count()
        response = self.client.delete(reverse('ingredient'), {'id': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert count == Ingredient.objects.all().count()

    def test_ingredient_delete_missing_params(self):
        """Testing DELETE ingredient view with missing params"""
        count = Ingredient.objects.all().count()
        response = self.client.delete(reverse('ingredient'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert count == Ingredient.objects.all().count()


class MealViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)
        self.meal_type1 = MealType.objects.create(diary=self.diary, name='Śniadanko')
        self.meal_type2 = MealType.objects.create(diary=self.diary, name='Lunch')
        self.meal = Meal.objects.create(meal_type=self.meal_type1)
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.ingredient1 = Ingredient.objects.create(meal=self.meal, product=self.product1, amount=2.2)
        self.ingredient2 = Ingredient.objects.create(meal=self.meal, product=self.product2, amount=1.3)

    def test_meal_get_correct_params(self):
        """Testing GET meal view with correct params"""
        response = self.client.get(reverse('meal'), {'id': self.meal.id})
        assert response.status_code == 200
        assert response.json() == {
            'total_kcal': None,
            'total_carbs': None,
            'total_proteins': None,
            'total_fat': None,
            'ingredients': [{'ingredient_id': 1, 'name': 'Kaszanka', 'amount': 2.2},
                            {'ingredient_id': 2, 'name': 'Śledziki', 'amount': 1.3}]
        }

    def test_meal_get_incorrect_params(self):
        """Testing GET meal view with incorrect params"""
        response = self.client.get(reverse('meal'), {'id': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_meal_get_missing_params(self):
        """Testing GET meal view with missing params"""
        response = self.client.get(reverse('meal'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}

    def test_meal_post_correct_params(self):
        """Testing POST meal view with correct params"""
        count = Meal.objects.all().count()
        response = self.client.post(reverse('meal'), {'meal_type_id': self.meal_type2.id})
        new_meal = Meal.objects.get(id=2)
        assert response.status_code == 200
        assert count + 1 == Meal.objects.all().count()
        assert response.json() == {'meal_id': new_meal.id}

    def test_meal_post_incorrect_params(self):
        """Testing POST meal view with incorrect params"""
        count = Meal.objects.all().count()
        response = self.client.post(reverse('meal'), {'meal_type_id': 'kanapka'})
        assert response.status_code == 400
        assert count == Meal.objects.all().count()
        assert response.json() == {'meal_type_id': ['A valid integer is required.']}

    def test_meal_post_missing_params(self):
        """Testing POST meal view with missing params"""
        count = Meal.objects.all().count()
        response = self.client.post(reverse('meal'), {})
        assert response.status_code == 400
        assert count == Meal.objects.all().count()
        assert response.json() == {'meal_type_id': ['This field is required.']}

    def test_meal_put_correct_params(self):
        """Testing PUT meal view with correct params"""
        old_meal = Meal.objects.get(id=self.meal.id)
        response = self.client.put(reverse('meal'), {'id': self.meal.id,
                                                     'total_kcal': 100,
                                                     'total_carbs': 10,
                                                     'total_proteins': 10,
                                                     'total_fat': 10})
        new_meal = Meal.objects.get(id=self.meal.id)
        assert response.status_code == 200
        assert response.json() == {'meal_id': self.meal.id}
        assert old_meal.total_kcal != new_meal.total_kcal

    def test_meal_put_incorrect_params(self):
        """Testing PUT meal view with incorrect params"""
        old_meal = Meal.objects.get(id=self.meal.id)
        response = self.client.put(reverse('meal'), {'id': self.meal.id,
                                                     'total_kcal': 100,
                                                     'total_carbs': 10,
                                                     'total_proteins': 10,
                                                     'total_fat': 'kanapka'})
        new_meal = Meal.objects.get(id=self.meal.id)
        assert response.status_code == 400
        assert response.json() == {'total_fat': ['A valid number is required.']}
        assert old_meal.total_kcal == new_meal.total_kcal

    def test_meal_put_missing_params(self):
        """Testing PUT meal view with missing params"""
        old_meal = Meal.objects.get(id=self.meal.id)
        response = self.client.put(reverse('meal'), {'total_kcal': 100,
                                                     'total_carbs': 10,
                                                     'total_proteins': 10,
                                                     'total_fat': 10})
        new_meal = Meal.objects.get(id=self.meal.id)
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert old_meal.total_kcal == new_meal.total_kcal

    def test_meal_delete_correct_params(self):
        """Testing DELETE meal view with correct params"""
        count = Meal.objects.all().count()
        response = self.client.delete(reverse('meal'), {'id': self.meal.id})
        assert response.status_code == 200
        assert response.json() == {}
        assert count - 1 == Meal.objects.all().count()

    def test_meal_delete_incorrect_params(self):
        """Testing DELETE meal view with incorrect params"""
        count = Meal.objects.all().count()
        response = self.client.delete(reverse('meal'), {'id': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert count == Meal.objects.all().count()

    def test_meal_delete_missing_params(self):
        """Testing DELETE meal view with missing params"""
        count = Meal.objects.all().count()
        response = self.client.delete(reverse('meal'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert count == Meal.objects.all().count()


class MealTypeViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.name = 'Przystawka'
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)
        self.meal_type1 = MealType.objects.create(diary=self.diary, name='Śniadanko')
        self.meal_type2 = MealType.objects.create(diary=self.diary, name='Lunch')
        self.meal = Meal.objects.create(meal_type=self.meal_type1)
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.ingredient1 = Ingredient.objects.create(meal=self.meal, product=self.product1, amount=2.2)
        self.ingredient2 = Ingredient.objects.create(meal=self.meal, product=self.product2, amount=1.3)

    def test_meal_type_get_correct_params(self):
        """Testing GET meal-type view with correct params"""
        response = self.client.get(reverse('meal-type'), {'id': self.meal_type1.id})
        assert response.status_code == 200
        assert response.json() == {
            'name': 'Śniadanko',
            'total_kcal': None,
            'total_carbs': None,
            'total_proteins': None,
            'total_fat': None,
            'ingredients': [{'ingredient_id': 1, 'name': 'Kaszanka', 'amount': 2.2},
                            {'ingredient_id': 2, 'name': 'Śledziki', 'amount': 1.3}]}

    def test_meal_type_get_incorrect_params(self):
        """Testing GET meal-type view with incorrect params"""
        response = self.client.get(reverse('meal-type'), {'id': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_meal_type_get_missing_params(self):
        """Testing GET meal-type view with missing params"""
        response = self.client.get(reverse('meal-type'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}

    def test_meal_type_post_correct_params(self):
        """Testing POST meal-type view with correct params"""
        count = MealType.objects.all().count()
        response = self.client.post(reverse('meal-type'), {'diary_id': self.diary.id,
                                                           'name': self.name})
        meal_type = MealType.objects.get(id=3)
        assert response.status_code == 200
        assert response.json() == {'meal_type_id': meal_type.id}
        assert count + 1 == MealType.objects.all().count()

    def test_meal_type_post_incorrect_params(self):
        """Testing POST meal-type view with incorrect params"""
        count = MealType.objects.all().count()
        response = self.client.post(reverse('meal-type'), {'diary_id': 'kanapka',
                                                           'name': self.name})
        assert response.status_code == 400
        assert response.json() == {'diary_id': ['A valid integer is required.']}
        assert count == MealType.objects.all().count()

    def test_meal_type_post_missing_params(self):
        """Testing POST meal-type view with missing params"""
        count = MealType.objects.all().count()
        response = self.client.post(reverse('meal-type'), {'name': self.name})
        assert response.status_code == 400
        assert response.json() == {'diary_id': ['This field is required.']}
        assert count == MealType.objects.all().count()

    def test_meal_type_delete_correct_params(self):
        """Testing DELETE meal-type view with correct params"""
        count = MealType.objects.all().count()
        response = self.client.delete(reverse('meal-type'), {'id': self.meal_type1.id})
        assert response.status_code == 200
        assert response.json() == {}
        assert count - 1 == MealType.objects.all().count()

    def test_meal_type_delete_incorrect_params(self):
        """Testing DELETE meal-type view with incorrect params"""
        count = MealType.objects.all().count()
        response = self.client.delete(reverse('meal-type'), {'id': 'abc'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert count == MealType.objects.all().count()

    def test_meal_type_delete_missing_params(self):
        """Testing DELETE meal-type view with missing params"""
        count = MealType.objects.all().count()
        response = self.client.delete(reverse('meal-type'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert count == MealType.objects.all().count()


class MealTypesViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.name = 'Przystawka'
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)
        self.meal_type1 = MealType.objects.create(diary=self.diary, name='Śniadanko')
        self.meal_type2 = MealType.objects.create(diary=self.diary, name='Lunch')
        self.meal1 = Meal.objects.create(meal_type=self.meal_type1)
        self.meal2 = Meal.objects.create(meal_type=self.meal_type2)
        self.product1 = Product.objects.create(name='Kaszanka', kcal=500, carbs=10, proteins=10, fat=10)
        self.product2 = Product.objects.create(name='Śledziki', kcal=400, carbs=0, proteins=20, fat=15)
        self.ingredient1 = Ingredient.objects.create(meal=self.meal1, product=self.product1, amount=2.2)
        self.ingredient2 = Ingredient.objects.create(meal=self.meal1, product=self.product2, amount=1.3)
        self.ingredient3 = Ingredient.objects.create(meal=self.meal2, product=self.product2, amount=0.3)

    def test_meal_types_get_correct_params(self):
        """Testing GET meal-types view with correct params"""
        response = self.client.get(reverse('meal-types'), {'diary_id': self.diary.id})
        assert response.status_code == 200
        assert response.json() == [
            {
                'meal_type_id': 1, 'name': 'Śniadanko', 'total_kcal': None, 'total_carbs': None, 'total_proteins': None,
                'total_fat': None, 'ingredients': [{'ingredient_id': 1, 'name': 'Kaszanka', 'amount': 2.2},
                                                   {'ingredient_id': 2, 'name': 'Śledziki', 'amount': 1.3}]},
            {
                'meal_type_id': 2, 'name': 'Lunch', 'total_kcal': None, 'total_carbs': None, 'total_proteins': None,
                'total_fat': None, 'ingredients': [{'ingredient_id': 3, 'name': 'Śledziki', 'amount': 0.3}]}
        ]

    def test_meal_types_get_incorrect_params(self):
        """Testing GET meal-types view with incorrect params"""
        response = self.client.get(reverse('meal-types'), {'diary_id': 'abc'})
        assert response.status_code == 400
        assert response.json() == {'diary_id': ['A valid integer is required.']}

    def test_meal_types_get_missing_params(self):
        """Testing GET meal-types view with missing params"""
        response = self.client.get(reverse('meal-types'), {})
        assert response.status_code == 400
        assert response.json() == {'diary_id': ['This field is required.']}


class UserViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username1 = 'jkowalski'
        self.password1 = 'kowi123'
        self.email1 = 'kowi@kowi.com'
        self.username2 = 'abc'
        self.password2 = 'kowadlo123'
        self.email2 = 'abc@bca.com'
        self.user = Profile.objects.create_user(username=self.username1, password=self.password1, email=self.email1)
        self.height = 180
        self.gender = 'M'
        self.daily_carbs = 20
        self.daily_fat = 20
        self.daily_proteins = 20

    def test_user_post_correct_params(self):
        """Testing POST user view with correct params"""
        count = Profile.objects.all().count()
        response = self.client.post(reverse('user'), {'username': self.username2,
                                                      'password': self.password2,
                                                      'email': self.email2})
        user = Profile.objects.get(id=2)
        assert response.status_code == 200
        assert response.json() == {'user_id': user.id}
        assert count + 1 == Profile.objects.all().count()

    def test_user_post_incorrect_params(self):
        """Testing POST user view with incorrect params"""
        count = Profile.objects.all().count()
        response = self.client.post(reverse('user'), {'username': self.username2,
                                                      'password': self.password2,
                                                      'email': 'abc'})
        assert response.status_code == 400
        assert response.json() == {'email': ['Enter a valid email address.']}
        assert count == Profile.objects.all().count()

    def test_user_post_missing_params(self):
        """Testing POST user view with missing params"""
        count = Profile.objects.all().count()
        response = self.client.post(reverse('user'), {'username': self.username2,
                                                      'password': self.password2})
        assert response.status_code == 400
        assert response.json() == {'email': ['This field is required.']}
        assert count == Profile.objects.all().count()

    def test_user_put_correct_params(self):
        """Testing PUT user view with correct params"""
        old_user = Profile.objects.get(id=self.user.id)
        response = self.client.put(reverse('user'), {'id': self.user.id,
                                                     'height': self.height,
                                                     'gender': self.gender,
                                                     'daily_carbs': self.daily_carbs,
                                                     'daily_fat': self.daily_fat,
                                                     'daily_proteins': self.daily_proteins})
        updated_user = Profile.objects.get(id=self.user.id)
        assert response.status_code == 200
        assert response.json() == {}
        assert old_user.daily_proteins != updated_user.daily_proteins

    def test_user_put_incorrect_params(self):
        """Testing PUT user view with incorrect params"""
        old_user = Profile.objects.get(id=self.user.id)
        response = self.client.put(reverse('user'), {'id': 'kanapka',
                                                     'height': self.height,
                                                     'gender': self.gender,
                                                     'daily_carbs': self.daily_carbs,
                                                     'daily_fat': self.daily_fat,
                                                     'daily_proteins': self.daily_proteins})
        updated_user = Profile.objects.get(id=self.user.id)
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert old_user.daily_proteins == updated_user.daily_proteins

    def test_user_put_missing_params(self):
        """Testing PUT user view with missing params"""
        old_user = Profile.objects.get(id=self.user.id)
        response = self.client.put(reverse('user'), {'height': self.height,
                                                     'gender': self.gender,
                                                     'daily_carbs': self.daily_carbs,
                                                     'daily_fat': self.daily_fat,
                                                     'daily_proteins': self.daily_proteins})
        updated_user = Profile.objects.get(id=self.user.id)
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert old_user.daily_proteins == updated_user.daily_proteins

    def test_user_delete_correct_params(self):
        """Testing DELETE user view with correct params"""
        count = Profile.objects.all().count()
        response = self.client.delete(reverse('user'), {'id': self.user.id,
                                                        'password': self.password1})
        assert response.status_code == 200
        assert response.json() == {}
        assert count == Profile.objects.all().count() + 1

    def test_user_delete_incorrect_params(self):
        """Testing DELETE user view with incorrect params"""
        count = Profile.objects.all().count()
        response = self.client.delete(reverse('user'), {'id': 'kanapka',
                                                        'password': self.password1})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert count == Profile.objects.all().count()

    def test_user_delete_missing_params(self):
        """Testing DELETE user view with missing params"""
        count = Profile.objects.all().count()
        response = self.client.delete(reverse('user'), {'password': self.password1})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert count == Profile.objects.all().count()


class ProfileViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username1 = 'jkowalski'
        self.password1 = 'kowi123'
        self.email1 = 'kowi@kowi.com'
        self.user = Profile.objects.create_user(username=self.username1,
                                                password=self.password1,
                                                email=self.email1)
        Profile.objects.filter(id=self.user.id).update(height=180,
                                                       gender='M',
                                                       daily_carbs=20,
                                                       daily_fat=20,
                                                       daily_proteins=20)

    def test_profile_post_correct_params(self):
        """Testing POST profile view with correct params"""
        response = self.client.post(reverse('profile'), {'id': self.user.id})
        assert response.status_code == 200
        assert response.json() == {'username': 'jkowalski',
                                   'height': 180,
                                   'gender': 'M',
                                   'daily_carbs': 20.0,
                                   'daily_proteins': 20.0,
                                   'daily_fat': 20.0}

    def test_profile_post_incorrect_params(self):
        """Testing POST profile view with incorrect params"""
        response = self.client.post(reverse('profile'), {'id': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_profile_post_missing_params(self):
        """Testing POST profile view with missing params"""
        response = self.client.post(reverse('profile'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}


class WeightViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username1 = 'jkowalski'
        self.password1 = 'kowi123'
        self.email1 = 'kowi@kowi.com'
        self.date = "2017-12-13"
        self.date2 = "2017-12-14"
        self.user = Profile.objects.create_user(username=self.username1,
                                                password=self.password1,
                                                email=self.email1)
        self.weight = Weight.objects.create(user=self.user, date=self.date, value=123)
        self.weight2 = Weight.objects.create(user=self.user, date=self.date2, value=122)

    def test_weight_get_correct_params(self):
        """Testing GET weight view with correct params"""
        response = self.client.get(reverse('weight'), {'user_id': self.user.id,
                                                       'date': self.date})
        assert response.status_code == 200
        assert response.json() == {'weight_id': self.weight.id}

    def test_weight_get_incorrect_params(self):
        """Testing GET weight view with incorrect params"""
        response = self.client.get(reverse('weight'), {'user_id': 'kanapka',
                                                       'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['A valid integer is required.']}

    def test_weight_get_missing_params(self):
        """Testing GET weight view with missing params"""
        response = self.client.get(reverse('weight'), {'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}

    def test_weight_post_correct_params(self):
        """Testing POST weight view with correct params"""
        count = Weight.objects.all().count()
        response = self.client.post(reverse('weight'), {'user_id': self.user.id,
                                                        'date': "2017-12-14",
                                                        'value': 80})
        weight = Weight.objects.get(id=3)
        assert response.status_code == 200
        assert response.json() == {'weight_id': weight.id}
        assert count + 1 == Weight.objects.all().count()

    def test_weight_post_incorrect_params(self):
        """Testing POST weight view with incorrect params"""
        count = Weight.objects.all().count()
        response = self.client.post(reverse('weight'), {'user_id': self.user.id,
                                                        'date': 30,
                                                        'value': 80})
        assert response.status_code == 400
        assert response.json() == {'date': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].']}
        assert count == Weight.objects.all().count()

    def test_weight_post_missing_params(self):
        """Testing POST weight view with missing params"""
        count = Weight.objects.all().count()
        response = self.client.post(reverse('weight'), {'user_id': self.user.id,
                                                        'value': 80})
        assert response.status_code == 400
        assert response.json() == {'date': ['This field is required.']}
        assert count == Weight.objects.all().count()

    def test_weight_delete_correct_params(self):
        """Testing DELETE weight view with correct params"""
        count = Weight.objects.all().count()
        response = self.client.delete(reverse('weight'), {'id': self.weight.id})
        assert response.status_code == 200
        assert response.json() == {}
        assert count == Weight.objects.all().count() + 1

    def test_weight_delete_incorrect_params(self):
        """Testing DELETE weight view with incorrect params"""
        count = Weight.objects.all().count()
        response = self.client.delete(reverse('weight'), {'id': 'abc'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert count == Weight.objects.all().count()

    def test_weight_delete_missing_params(self):
        """Testing DELETE weight view with missing params"""
        count = Weight.objects.all().count()
        response = self.client.delete(reverse('weight'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert count == Weight.objects.all().count()

    def test_weights_get_correct_params(self):
        """Testing GET weights view with correct params"""
        response = self.client.get(reverse('weights'), {'user_id': self.user.id})
        assert response.status_code == 200
        assert response.json() == [
            {'value': self.weight.value,
             'date': self.weight.date},
            {'value': self.weight2.value,
             'date': self.weight2.date}
        ]

    def test_weights_get_incorrect_params(self):
        """Testing GET weights view with incorrect params"""
        response = self.client.get(reverse('weights'), {'user_id': 'abc'})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['A valid integer is required.']}

    def test_weights_get_missing_params(self):
        """Testing GET weights view with missing params"""
        response = self.client.get(reverse('weights'), {})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}


class LoginViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username = 'jkowalski'
        self.password = 'kowi123'
        self.email = 'kowi@kowi.com'
        self.user = Profile.objects.create_user(username=self.username,
                                                password=self.password,
                                                email=self.email)

    def test_login_post_correct_params(self):
        """Testing POST login view with correct params"""
        response = self.client.post(reverse('login'), {'username': self.user.username,
                                                       'password': self.user.password})
        assert response.status_code == 200
        assert response.json() == {'user_id': self.user.id}

    def test_login_post_incorrect_params(self):
        """Testing POST login view with incorrect params"""
        response = self.client.post(reverse('login'), {'username': self.user.username,
                                                       'password': ''})
        assert response.status_code == 400
        assert response.json() == {'password': ['This field may not be blank.']}

    def test_login_post_missing_params(self):
        """Testing POST login view with missing params"""
        response = self.client.post(reverse('login'), {'username': self.user.username})
        assert response.status_code == 400
        assert response.json() == {'password': ['This field is required.']}

