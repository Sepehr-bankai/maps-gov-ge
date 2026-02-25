import requests
import json
import time
import argparse

# Function to get longitude and latitude from user input
def get_coordinates():
    # Prompt the user to input longitude and latitude
    longitude = input("Please enter the longitude: ")
    latitude = input("Please enter the latitude: ")
    return longitude, latitude

# Function to send POST request and save the response to a JSON file
def send_post_request(longitude, latitude):
    # Construct the URL (fixed in this case)
    url = "https://maps.gov.ge/map/portal/search"
    
    # Prepare the payload (the data to send in the body of the POST request)
    payload = {
        "keyword": f"{longitude},{latitude}",  # Adding the coordinates
        "keyword_description[coords][]": longitude,
        "keyword_description[coords][]": latitude,
        "keyword_description[zoom]": "21",  # Zoom level, this might vary depending on your need
        "keyword_description[screen_width]": "1920",  # Example screen width
        "keyword_description[screen_height]": "1080",  # Example screen height
        "keyword_description[projection]": "EPSG:4326",
        "keyword_description[orientation_angle]": "0",
        "keyword_description[lang]": "ka"  # Georgian language
    }
    
    # Add headers, mimicking the ones in the browser
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    try:
        # Send the POST request with the payload and headers
        response = requests.post(url, data=payload, headers=headers)
        
        # Check if the response is successful
        if response.status_code == 200:
            print("Request sent successfully.")
            
            # Get the response in JSON format (if applicable)
            response_data = response.json()
            
            # Save the response to a JSON file
            file_name = f"response_{longitude}_{latitude}.json"
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=4)
            
            print(f"Response saved to file: {file_name}")
        else:
            print(f"Error in sending request. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to process a JSON file of coordinates and send requests with rate limiting

def process_coordinates_file(file_path, delay_seconds=1):
    """Load coordinates from a JSON file, sort them, and send POST requests.

    Keys within the JSON should be strings of the form "lat,lon". We sort
    numerically by latitude then longitude to ensure deterministic ordering.
    After each request a delay is inserted to respect the specified rate limit.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            coords = json.load(f)
    except Exception as e:
        print(f"Failed to read coordinates file {file_path}: {e}")
        return

    # Parse keys and sort
    points = []
    for key in coords.keys():
        try:
            lat_str, lon_str = key.split(',')
            lat = float(lat_str)
            lon = float(lon_str)
        except ValueError:
            continue
        points.append((lat, lon))

    points.sort()

    for lat, lon in points:
        # send_post_request takes longitude first
        send_post_request(lon, lat)
        time.sleep(delay_seconds)


# Main function to execute the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send POST requests using manual input or a JSON file of coordinates"
    )
    parser.add_argument("--file", "-f", help="JSON file with coordinates", default="coordinates.json")
    parser.add_argument("--delay", "-d", type=float, help="Seconds between requests (rate limit)", default=1.0)
    args = parser.parse_args()

    if args.file:
        print(f"Using file {args.file}, delay={args.delay}s")
        process_coordinates_file(args.file, delay_seconds=args.delay)
    else:
        longitude, latitude = get_coordinates()
        send_post_request(longitude, latitude)
