import math
import json

# Function to calculate the coordinates around the circle
def generate_coordinates_in_circle(center_lat, center_lon, radius_meters, step_size=10):
    # Constants
    lat_degree_in_meters = 111.32 * 1000  # One degree of latitude in meters at the equator
    lon_degree_in_meters = lat_degree_in_meters * math.cos(math.radians(center_lat))  # One degree of longitude in meters
    
    # List to store all the coordinates
    coordinates = {}
    
    # Convert the radius from meters to degrees for latitude and longitude
    lat_radius_deg = radius_meters / lat_degree_in_meters
    lon_radius_deg = radius_meters / lon_degree_in_meters
    
    # Loop to generate coordinates in steps (10 meters each)
    lat = center_lat - lat_radius_deg
    while lat <= center_lat + lat_radius_deg:
        lon = center_lon - lon_radius_deg
        while lon <= center_lon + lon_radius_deg:
            # Calculate distance from center to ensure it's inside the circle
            distance = calculate_distance(center_lat, center_lon, lat, lon)
            if distance <= radius_meters:
                # Add the coordinates to the dictionary
                coordinates[f"{lat},{lon}"] = {"latitude": lat, "longitude": lon}
            lon += step_size / lon_degree_in_meters  # Move in steps of 10 meters for longitude
        lat += step_size / lat_degree_in_meters  # Move in steps of 10 meters for latitude
    
    return coordinates

# Function to calculate the distance between two points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the great-circle distance
    R = 6371  # Radius of the Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c * 1000
    return distance

# Function to save coordinates to a JSON file
def save_coordinates_to_json(coordinates, filename="coordinates.json"):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(coordinates, json_file, ensure_ascii=False, indent=4)

# Main function to execute the program
if __name__ == "__main__":
    # Input the center coordinates and radius in meters
    center_lat = float(input("Enter the latitude of the center point: "))
    center_lon = float(input("Enter the longitude of the center point: "))
    radius_meters = float(input("Enter the radius in meters: "))
    
    # Generate the coordinates in the circle
    coordinates = generate_coordinates_in_circle(center_lat, center_lon, radius_meters)
    
    # Save the coordinates to a JSON file
    save_coordinates_to_json(coordinates)
    
    print(f"Coordinates saved to 'coordinates.json'.")