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
