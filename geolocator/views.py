from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from atlantaFoodFinder import settings
from .models import Restaurant, Favorite
from django.contrib.auth.decorators import login_required


def get_nearby_places(location, radius, keyword=None, min_rating=0):
    """
    Fetch nearby places using Google Maps API.
    :param location: Tuple of (latitude, longitude)
    :param radius: Search radius in meters
    :param keyword: Optional keyword to filter search (e.g. 'restaurant')
    :param min_rating: Minimum rating to filter results
    :return: List of places
    """
    gmaps = settings.GOOGLE_API_KEY

    # Call Google Places API
    places_result = gmaps.places_nearby(
        location=location,
        radius=radius,
        keyword=keyword,
        open_now=True
    )

    # Filter by rating
    filtered_places = [
        place for place in places_result['results']
        if place.get('rating', 0) >= min_rating
    ]

    return filtered_places

# Main view to handle place search
def geolocator(request):
    user_lat = request.GET.get('latitude')  # User's latitude
    user_lng = request.GET.get('longitude')  # User's longitude
    radius = int(request.GET.get('radius', 1000))  # Search radius (meters)
    min_rating = float(request.GET.get('min_rating', 0))  # Minimum rating
    keyword = request.GET.get('keyword', '')  # Optional keyword for filtering

    if user_lat and user_lng:
        location = (float(user_lat), float(user_lng))

        # Fetch nearby places based on user location
        places = get_nearby_places(location, radius, keyword, min_rating)

        context = {
            'places': places,
            'latitude': user_lat,
            'longitude': user_lng,
        }
        return render(request, 'geolocator/map.html', {'context': context, 'google_api_key': settings.GOOGLE_API_KEY,})

    return render(request, 'geolocator/map.html', {'google_api_key': settings.GOOGLE_API_KEY})

@login_required
def add_favorite(request, place_id, place_name=''):
    print('add_favorite called')
    print(place_id)


    try:
        favorite = Favorite.objects.get(user=request.user, restaurant=place_id)
        print(favorite)
        favorite.delete()
    except:
        favorite = Favorite.objects.create(user=request.user, restaurant=place_id, restaurant_name=place_name)
        print('created', favorite)
    return redirect(request.META.get('HTTP_REFERER', 'geolocator'))

@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    print(favorites)
    return render(request, 'favorites/list-favorites.html', {'favorites': favorites})