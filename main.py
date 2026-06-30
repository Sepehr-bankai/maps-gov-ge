import requests
import json
import time
import argparse
import glob
import html
import os
import re

# Function to get longitude and latitude from user input
def get_coordinates():
    # Prompt the user to input longitude and latitude
    longitude = input("Please enter the longitude: ")
    latitude = input("Please enter the latitude: ")
    return longitude, latitude

# Function to send a POST request and return its JSON response
def send_post_request(longitude, latitude):
    # Construct the URL (fixed in this case)
    url = "https://maps.gov.ge/map/portal/search"
    
    # Prepare the payload (the data to send in the body of the POST request)
    payload = {
        "keyword": f"{longitude},{latitude}",  # Adding the coordinates
        "keyword_description[coords][]": [longitude, latitude],
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
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        
        # Check if the response is successful
        if response.status_code == 200:
            print("Request sent successfully.")
            
            # Get the response in JSON format (if applicable)
            response_data = response.json()
            for result in response_data.get("result", []):
                info_link = result.get("details", {}).get("info_link")
                if not info_link:
                    continue
                details = requests.get(f"https://maps.gov.ge{info_link}", timeout=30)
                details.raise_for_status()
                owner_html = details.text.partition("<!--begin of MI.OWNERS.ACT.MAPGOV.ALPHA -->")[2].partition("<!--END of MI.OWNERS.ACT.MAPGOV.ALPHA -->")[0]
                result["owners"] = [
                    html.unescape(re.sub(r"<[^>]+>", "", owner)).strip()
                    for owner in re.findall(r"<p[^>]*>(.*?)</p>", owner_html, re.DOTALL)
                ]
            
            return response_data
        else:
            print(f"Error in sending request. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None


def save_response_batch(responses, batch_number):
    file_name = f"responses_{batch_number:04}.json"
    temp_name = f"{file_name}.tmp"
    with open(temp_name, 'w', encoding='utf-8') as json_file:
        json.dump(responses, json_file, ensure_ascii=False, indent=4)
    os.replace(temp_name, file_name)
    print(f"Saved {len(responses)} responses to {file_name}")

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

    response_files = sorted(glob.glob("responses_[0-9][0-9][0-9][0-9].json"))
    processed = set()
    last_batch = []
    for response_file in response_files:
        with open(response_file, encoding="utf-8") as f:
            batch = json.load(f)
            processed.update((item["latitude"], item["longitude"]) for item in batch)
            last_batch = batch

    responses = last_batch if last_batch and len(last_batch) < 100 else []
    last_batch_number = int(response_files[-1][-9:-5]) if response_files else 0
    batch_number = last_batch_number if responses else last_batch_number + 1
    print(f"Skipping {len(processed)} coordinates already saved; {len(points) - len(processed)} remaining")
    for lat, lon in points:
        if (lat, lon) in processed:
            continue
        # send_post_request takes longitude first
        response = send_post_request(lon, lat)
        if response is not None:
            responses.append({"latitude": lat, "longitude": lon, "response": response})
            save_response_batch(responses, batch_number)
            if len(responses) == 100:
                responses = []
                batch_number += 1
        time.sleep(delay_seconds)


# Main function to execute the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send POST requests using manual input or a JSON file of coordinates"
    )
    parser.add_argument("--file", "-f", help="JSON file with coordinates", default="coordinates.json")
    parser.add_argument("--delay", "-d", type=float, help="Seconds between requests (default: 100 requests/minute)", default=0.6)
    args = parser.parse_args()

    if args.file:
        print(f"Using file {args.file}, delay={args.delay}s")
        process_coordinates_file(args.file, delay_seconds=args.delay)
    else:
        longitude, latitude = get_coordinates()
        send_post_request(longitude, latitude)
