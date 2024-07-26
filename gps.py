from geopy.distance import geodesic
import math

def calculate_distance(coord1, coord2):
    # coord1 and coord2 should be tuples with (latitude, longitude) values
    distance = geodesic(coord1, coord2).kilometers
    return distance

def calculate_direction(coord1, coord2):
    # coord1 and coord2 should be tuples with (latitude, longitude) values

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Calculate the difference in longitudes
    delta_lon = lon2 - lon1

    # Calculate the direction using arctan2
    direction = math.atan2(math.sin(math.radians(delta_lon)) * math.cos(math.radians(lat2)),
                           math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
                           math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon)))

    # Convert the direction from radians to degrees
    direction = math.degrees(direction)

    # Adjust the direction to be between 0 and 360 degrees
    direction = (direction + 360) % 360

    return direction

# Example coordinates
coord1 = (11.048958, 76.9575143)  # San Francisco
coord2 = (11.08330, 76.978745)  # Los Angeles

distance = calculate_distance(coord1, coord2)
direction = calculate_direction(coord1, coord2)

print(f"Distance: {distance:.2f} km")
print(f"Direction: {direction:.2f} degrees")
