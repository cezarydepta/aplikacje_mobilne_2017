from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    """Class represents a user of the app."""
    height = models.IntegerField(null=True, blank=True)
    """The height of the user."""
    gender = models.CharField(max_length=1, blank=True)
    """Gender of the user."""
    daily_kcal = models.FloatField(null=True, blank=True)
    """Daily user calories cap."""
    daily_carbs = models.FloatField(null=True, blank=True)
    """Daily user carbs cap."""
    daily_fat = models.FloatField(null=True, blank=True)
    """Daily user fats cap."""
    daily_proteins = models.FloatField(null=True, blank=True)
    """Daily user proteins cap."""


class Weight(models.Model):
    """Class represents weights of the user"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    """ID of the user"""
    value = models.FloatField()
    """User weight"""
    date = models.DateField()
    """Date when weight was given"""

    def __str__(self):
        """String representation of an object"""
        return '{}. Weight of {} from {}'.format(self.id, self.user.username, self.date)


class Diary(models.Model):
    """Class represents diary that contains all daily information"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    """ID of the user"""
    date = models.DateField()
    """Date of the diary"""

    def __str__(self):
        """String representation of an object"""
        return '{}. Diary for user {} from {}'.format(self.id, self.user, self.date)


class MealType(models.Model):
    """Class defines what type of meal it is (eg. breakfast, lunch, dinner)"""
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    """ID of the diary"""
    name = models.CharField(max_length=30)
    """Name of meal (eg. breakfast, lunch, dinner)"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {}'.format(self.id, self.name)


class Meal(models.Model):
    """Class represents information about meal"""
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    """ID of the meal type"""
    total_kcal = models.FloatField(null=True, blank=True)
    """Meal calories"""
    total_carbs = models.FloatField(null=True, blank=True)
    """Meal carbs"""
    total_proteins = models.FloatField(null=True, blank=True)
    """Meal proteins"""
    total_fat = models.FloatField(null=True, blank=True)
    """Meal fats"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {}'.format(self.id, self.meal_type.name)


class Product(models.Model):
    """Class represent information about product"""
    name = models.CharField(max_length=30)
    """Name of the product"""
    kcal = models.FloatField()
    """Calories of product in 100g"""
    carbs = models.FloatField()
    """Carbs of product"""
    proteins = models.FloatField()
    """Proteins of product"""
    fat = models.FloatField()
    """Fats of product"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {}'.format(self.id, self.name)


class Ingredient(models.Model):
    """Class represents how much of product user ate"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    """ID of the product"""
    meal = models.ForeignKey(Meal, null=True, on_delete=models.CASCADE)
    """ID of the meal"""
    amount = models.FloatField()
    """How much user ate of given product"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {}'.format(self.id, self.product.name)


class Discipline(models.Model):
    """Class represents how much discipline burn calories an hour"""
    name = models.CharField(max_length=30)
    """Name of discipline"""
    calories_burn = models.FloatField()
    """Calories burnt per hour by discipline"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {}'.format(self.id, self.name)

    def to_representation(self):
        return {'id': self.id, 'name': self.name}


class Activity(models.Model):
    """Class represent how long, and what discipline user was doing"""
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    """ID of the diary"""
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    """ID of the discipline"""
    time = models.TimeField()
    """How long user was training"""

    def __str__(self):
        """String representation of an object"""
        return '{}. {} from {}'.format(self.id, self.discipline.name, self.diary.id)
