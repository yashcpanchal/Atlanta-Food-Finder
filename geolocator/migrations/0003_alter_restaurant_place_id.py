# Generated by Django 5.1.1 on 2024-10-02 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geolocator', '0002_restaurant_place_id_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='place_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
