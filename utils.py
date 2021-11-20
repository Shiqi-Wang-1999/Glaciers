import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    a = math.pow(math.sin((lat2-lat1)/2), 2)
    b = math.pow(math.sin((lon2-lon1)/2), 2)
    c = math.cos(lat1)*math.cos(lat2)
    return 2*6371*math.asin(math.sqrt(a+b*c))
