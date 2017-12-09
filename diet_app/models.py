from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    height = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    daily_kcal = models.FloatField(null=True, blank=True)
    daily_carbs = models.FloatField(null=True, blank=True)
    daily_fat = models.FloatField(null=True, blank=True)
    daily_proteins = models.FloatField(null=True, blank=True)


class Weight(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return str(self.date) + ' ' + str(self.value)


class Diary(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return 'Diary for user {} from {}'.format(self.user_id, self.date)


class Meal(models.Model):
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    total_kcal = models.FloatField(null=True, blank=True)
    total_carbs = models.FloatField(null=True, blank=True)
    total_proteins = models.FloatField(null=True, blank=True)
    total_fat = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.diary_id)


class MealType(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    kcal = models.FloatField()
    carbs = models.FloatField()
    proteins = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.product_id)


class Discipline(models.Model):
    name = models.CharField(max_length=30)
    calories_burn = models.FloatField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):
        return str(self.discipline_id)
