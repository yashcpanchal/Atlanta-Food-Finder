from django.contrib.auth.models import User
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.CharField(max_length=255)
    restaurant_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')
        # Alternatively, using UniqueConstraint:
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'restaurant'], name='unique_favorite')
        # ]
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.username} favorited {self.restaurant_name}"
