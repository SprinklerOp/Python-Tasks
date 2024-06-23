import geocoder

def get_current_location():
    current_location = geocoder.ip('me')
    latitude, longitude = current_location.latlng
    location_info = geocoder.osm([latitude, longitude], method='reverse')
    return latitude, longitude, location_info.address

latitude, longitude, location = get_current_location()
print("Latitude:", latitude)
print("Longitude:", longitude)
print("Location:", location)
