# Generated by Django 2.0 on 2017-12-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(null=True),
        ),
    ]
