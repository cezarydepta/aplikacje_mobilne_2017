from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from diet_app.models import *


class DiarySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField()

    def to_representation(self, instance):
        try:
            diary = Diary.objects.get(**instance)
            return {'diary_id': diary.id}

        except ObjectDoesNotExist:
            return {}

    def create(self, validated_data):
        return Diary.objects.get_or_create(**validated_data)[0]


class ActivityGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            activity = Activity.objects.get(**instance)
            return {'name': activity.discipline.name,
                    'calories_burn': activity.discipline.calories_burn,
                    'time': activity.time}

        except ObjectDoesNotExist:
            return {}


class ActivityCreateSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    discipline_id = serializers.IntegerField()
    time = serializers.TimeField()

    def to_representation(self, instance):
        return {}

    def create(self, validated_data):
        return Activity.objects.get_or_create(**validated_data)[0]


class ActivityDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        Activity.objects.filter(**validated_data).delete()


class ActivitiesListSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()

    def to_representation(self, instance):
        activities = Activity.objects.filter(**instance)
        return [{'name': activity.discipline.name,
                 'calories_burn': activity.discipline.calories_burn,
                 'time': activity.time} for activity in activities
                ]

    @property
    def data(self):
        return super(serializers.Serializer, self).data


class DisciplineSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            discipline = Discipline.objects.get(**instance)
            return {'name': discipline.name,
                    'calories_burn': discipline.calories_burn}

        except ObjectDoesNotExist:
            return {}


class DisciplinesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)

    def to_representation(self, instance):
        disciplines = Discipline.objects.filter(name__contains='{}'.format(instance.get('name')))
        return [{'id': discipline.id,
                 'name': discipline.name,
                 'calories_burn': discipline.calories_burn} for discipline in disciplines
                ]

    @property
    def data(self):
        return super(serializers.Serializer, self).data


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    kcal = serializers.FloatField()
    carbs = serializers.FloatField()
    proteins = serializers.FloatField()
    fat = serializers.FloatField()

    def to_representation(self, instance):
        product = Product.objects.get(**instance)
        return {'product_id': product.id}

    def create(self, validated_data):
        return Product.objects.get_or_create(**validated_data)[0]


class ProductGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        product = Product.objects.get(**instance)
        return {'name': product.name,
                'kcal': product.kcal,
                'carbs': product.carbs,
                'proteins': product.proteins,
                'fat': product.fat}


class ProductsGetSerializer(serializers.Serializer):
    name = serializers.CharField()

    def to_representation(self, instance):
        products = Product.objects.filter(name__contains='{}'.format(instance.get('name')))
        return [{'product_id': product.id,
                 'name': product.name} for product in products
                ]

    @property
    def data(self):
        return super(serializers.Serializer, self).data


class IngredientCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    meal_id = serializers.IntegerField()
    amount = serializers.FloatField()

    def to_representation(self, instance):
        ingredient = Ingredient.objects.get(**instance)
        return {'ingredient_id': ingredient.id}

    def create(self, validated_data):
        return Ingredient.objects.get_or_create(**validated_data)[0]


class IngredientDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        Ingredient.objects.filter(**validated_data).delete()


class MealGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            meal = Meal.objects.get(**instance)
            ingredients = Ingredient.objects.filter(meal=meal)
            ingredients_list = []
            for ingredient in ingredients:
                ingredients_list.append({'ingredient_id': ingredient.id,
                                         'name': ingredient.product.name,
                                         'amount': ingredient.amount})
            return {'total_kcal': meal.total_kcal,
                    'total_carbs': meal.total_carbs,
                    'total_proteins': meal.total_proteins,
                    'total_fat': meal.total_fat,
                    'ingredients': ingredients_list}

        except ObjectDoesNotExist:
            return {}


class MealCreateSerializer(serializers.Serializer):
    meal_type_id = serializers.IntegerField()

    def create(self, validated_data):
        return Ingredient.objects.get_or_create(**validated_data)[0]

    def to_representation(self, instance):
        meal = Meal.objects.get(**instance)
        return {'meal_id': meal.id}


class MealUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_kcal = serializers.FloatField(required=False)
    total_carbs = serializers.FloatField(required=False)
    total_proteins = serializers.FloatField(required=False)
    total_fat = serializers.FloatField(required=False)

    def to_representation(self, instance):
        try:
            meal = Meal.objects.get(id=instance.get('id'))
            return {'id': meal.id}

        except ObjectDoesNotExist:
            return {}

    def update(self, instance, validated_data):
        meal_id = validated_data.get('id')
        validated_data.pop('id')
        Meal.objects.filter(id=meal_id).update(**validated_data)


class MealDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        Meal.objects.filter(**validated_data).delete()


class MealTypeGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            meal_type = MealType.objects.get(**instance)
            meal = Meal.objects.get(meal_type=meal_type)
            ingredients = Ingredient.objects.filter(meal=meal)
            ingredients_list = []
            for ingredient in ingredients:
                ingredients_list.append({'ingredient_id': ingredient.id,
                                         'name': ingredient.product.name,
                                         'amount': ingredient.amount})
            return {'name': meal_type.name,
                    'total_kcal': meal.total_kcal,
                    'total_carbs': meal.total_carbs,
                    'total_proteins': meal.total_proteins,
                    'total_fat': meal.total_fat,
                    'ingredients': ingredients_list}

        except ObjectDoesNotExist:
            return {}


class MealTypeCreateSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return MealType.objects.get_or_create(**validated_data)[0]

    def to_representation(self, instance):
        meal_type = MealType.objects.get(**instance)
        return {'meal_type_id': meal_type.id}


class MealTypeDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        MealType.objects.filter(**validated_data).delete()


class MealTypesSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            diary = Diary.objects.get(id=instance.get('diary_id'))
            meal_types = MealType.objects.filter(diary=diary)
            data = []
            for meal_type in meal_types:
                meal = Meal.objects.get(meal_type=meal_type)
                ingredients = Ingredient.objects.filter(meal=meal)
                ingredients_list = []
                for ingredient in ingredients:
                    ingredients_list.append({'ingredient_id': ingredient.id,
                                             'name': ingredient.product.name,
                                             'amount': ingredient.amount})
                data.append({'meal_type_id': meal_type.id,
                             'name': meal_type.name,
                             'total_kcal': meal.total_kcal,
                             'total_carbs': meal.total_carbs,
                             'total_proteins': meal.total_proteins,
                             'total_fat': meal.total_fat,
                             'ingredients': ingredients_list})
            return data

        except ObjectDoesNotExist:
            return {}

    @property
    def data(self):
        return super(serializers.Serializer, self).data


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField()

    def create(self, validated_data):
        try:
            return Profile.objects.create_user(**validated_data)

        except IntegrityError:
            return {}

    def to_representation(self, instance):
        instance.pop('password')
        try:
            profile = Profile.objects.get(**instance)
            return {'user_id': profile.id}

        except ObjectDoesNotExist:
            return {}


class UserUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    height = serializers.IntegerField(required=False)
    gender = serializers.CharField(max_length=1, required=False)
    daily_carbs = serializers.FloatField(required=False)
    daily_fat = serializers.FloatField(required=False)
    daily_proteins = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        user_id = validated_data.get('id')
        validated_data.pop('id')
        Profile.objects.filter(id=user_id).update(**validated_data)

    def to_representation(self, instance):
        return {}


class UserDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(max_length=128)

    def delete(self, validated_data):
        Profile.objects.filter(**validated_data).delete()

    def to_representation(self, instance):
        return {}


class ProfileGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        try:
            user = Profile.objects.get(**instance)
            return {'username': user.username,
                    'height': user.height,
                    'gender': user.gender,
                    'daily_carbs': user.daily_carbs,
                    'daily_proteins': user.daily_proteins,
                    'daily_fat': user.daily_fat}

        except ObjectDoesNotExist:
            return {}


class WeightListGetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def to_representation(self, instance):
        weights = Weight.objects.filter(**instance)
        return [{'value': weight.value,
                 'date': weight.date} for weight in weights
                ]

    @property
    def data(self):
        return super(serializers.Serializer, self).data


class WeightGetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField()

    def to_representation(self, instance):
        try:
            weight = Weight.objects.get(**instance)
            return {'weight_id': weight.id}

        except ObjectDoesNotExist:
            return {}


class WeightCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField()
    value = serializers.FloatField()

    def create(self, validated_data):
        return Weight.objects.get_or_create(**validated_data)[0]

    def to_representation(self, instance):
        weight = Weight.objects.get(**instance)
        return {'weight_id': weight.id}


class WeightDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        Weight.objects.filter(**validated_data).delete()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def to_representation(self, instance):
        try:
            user = Profile.objects.get(**instance)
            return {'user_id': user.id}

        except ObjectDoesNotExist:
            return {}
