from django.shortcuts import render
from atlantaFoodFinder import settings
from .models import Restaurant

# def geolocator(request):
#     restaurants = Restaurant.objects.all()
#     return render(request, 'geolocator/map.html', {'restaurants': restaurants,
#                                                    'google_api_key': settings.GOOGLE_API_KEY,})


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