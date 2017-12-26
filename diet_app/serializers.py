from django.core.exceptions import ObjectDoesNotExist
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
    diary_id = serializers.IntegerField

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
        discipline = Discipline.objects.get(**instance)
        return {'name': discipline.name,
                'calories_burn': discipline.calories_burn}


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
        meal = Meal.objects.get(id=instance.get('id'))
        return {'id': meal.id}

    def update(self, instance, validated_data):
        validated_data.pop('id')
        Meal.objects.update(**validated_data)


class MealDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {}

    def delete(self, validated_data):
        Meal.objects.filter(**validated_data).delete()

# class MealsGetSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#
#     def to_representation(self, instance):
#         meals = Meal.objects.get(id=self.user_id)
#         return []
#
#     @property
#     def data(self):
#         return super(serializers.Serializer, self).data
