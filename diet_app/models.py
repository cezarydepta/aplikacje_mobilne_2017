from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    height = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, null=True)
    daily_kcal = models.FloatField(null=True)
    daily_carbs = models.FloatField(null=True)
    daily_fat = models.FloatField(null=True)
    daily_proteins = models.FloatField(null=True)


class Weight(models.Model):
    user_id = models.ForeignKey(Profile)
    value = models.FloatField()
    date = models.DateField()


class Diary(models.Model):
    user_id = models.ForeignKey(Profile)
    date = models.DateField()


class Meal(models.Model):
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    total_kcal = models.FloatField(null=True)
    total_carbs = models.FloatField(null=True)
    total_proteins = models.FloatField(null=True)
    total_fat = models.FloatField(null=True)


class MealType(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=30)
    kcal = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    fat = models.FloatField(null=True)


class Ingredient(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()


class Discipline(models.Model):
    name = models.CharField(max_length=30)
    calories_burn = models.FloatField()


class Activity(models.Model):
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    time = models.TimeField()
