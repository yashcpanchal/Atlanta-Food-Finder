from django.shortcuts import render

from atlantaFoodFinder import settings
from .models import Restaurant

def geolocator(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'geolocator/map.html', {'restaurants': restaurants,
                                                   'google_api_key': settings.GOOGLE_API_KEY,})
