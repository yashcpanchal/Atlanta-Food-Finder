# Generated by Django 5.1.1 on 2024-10-02 04:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("geolocator", "0004_favorite_restaurant_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favorite",
            options={"verbose_name": "Favorite", "verbose_name_plural": "Favorites"},
        ),
        migrations.AlterUniqueTogether(
            name="favorite",
            unique_together={("user", "restaurant")},
        ),
        migrations.AlterField(
            model_name="favorite",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorited_by",
                to="geolocator.restaurant",
            ),
        ),
        migrations.RemoveField(
            model_name="favorite",
            name="restaurant_name",
        ),
    ]
