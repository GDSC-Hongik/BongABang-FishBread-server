# Generated by Django 4.0 on 2024-01-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafeowner',
            name='cafe_name',
            field=models.CharField(max_length=100),
        ),
    ]