# Generated by Django 2.0 on 2017-12-17 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet_app', '0006_auto_20171211_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mealtype',
            name='meal',
        ),
        migrations.AddField(
            model_name='mealtype',
            name='meals',
            field=models.ManyToManyField(to='diet_app.Meal'),
        ),
    ]
