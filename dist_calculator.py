import math

def degree_to_radian(degree):
    return degree * math.pi / 180


def dist_btw_coords(lon1, lat1, lon2, lat2):
    earth_rad = 6371
    dLat = degree_to_radian(lat2 - lat1)
    dLon = degree_to_radian(lon2 - lon1)

    lat1 = degree_to_radian(lat1)
    lat2 = degree_to_radian(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_rad * c * 1000