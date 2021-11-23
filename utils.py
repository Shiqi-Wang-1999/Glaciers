import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    if (lat1 < -90.) | (lat1 > 90.) | (lon1 < -180.) | (lon1 > 180.):
        raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")
    if (lat2 < -90.) | (lat2 > 90.) | (lon2 < -180.) | (lon2 > 180.):
        raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")
    a = math.pow(math.sin((lat2-lat1)/2), 2)
    b = math.pow(math.sin((lon2-lon1)/2), 2)
    c = math.cos(lat1)*math.cos(lat2)
    return 2*6371*math.asin(math.sqrt(a+b*c))

