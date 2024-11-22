from geopy.geocoders import Nominatim

def get_lat_lon(address):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(address)
    
    # print(location.address)
    #print((location.latitude, location.longitude))
    return location.latitude, location.longitude
    
    