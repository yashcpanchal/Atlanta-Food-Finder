from django.urls import path
from . import views

urlpatterns = [
    # Add URL patterns here that map to your views
    path('map.html/', views.geolocator, name='geolocator'),
]
