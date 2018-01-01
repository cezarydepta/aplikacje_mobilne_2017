import os
from django.db import IntegrityError
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplikacje_mobilne_2017.settings')
import django
django.setup()
from diet_app.models import *
import json


def populate():
    data = json.load(open('populate/users.json'))
    for x in data:
        add_user(x['username'], x['password'], x['email'])

    data = json.load(open('populate/products.json'))
    for x in data:
        add_product(x['name'], x['kcal'], x['carbs'], x['proteins'], x['fat'])

    data = json.load(open('populate/disciplines.json'))
    for x in data:
        add_discipline(x['name'], x['calories_burn'])


def add_user(username, password, email):
    try:
        user = Profile.objects.create_user(username=username, password=password, email=email)
        user.save()
        return user

    except IntegrityError:
        pass


def add_product(name, kcal, carbs, proteins, fat):
    product = Product.objects.get_or_create(name=name, kcal=kcal, carbs=carbs, proteins=proteins, fat=fat)[0]
    product.save()
    return product


def add_discipline(name, calories_burn):
    discipline = Discipline.objects.get_or_create(name=name, calories_burn=calories_burn)[0]
    discipline.save()
    return discipline


if __name__ == '__main__':
    print("Start populating script...")
    populate()
    print("Done!")
