from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

def get_lat_long(location):
    geolocator = Nominatim(user_agent="twitter-location-extraction")
    try:
        location = geolocator.geocode(location)
        if location:
            return location.latitude, location.longitude
    except GeopyError as e:
        print(f"Error getting coordinates for {location}: {e}")
    return None

def extract_locations(tweet, pattern):
    return pattern.findall(tweet)
