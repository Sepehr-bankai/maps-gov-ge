import requests
import json

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

# Main function to execute the program
if __name__ == "__main__":
    # Get longitude and latitude from the user
    longitude, latitude = get_coordinates()
    
    # Send the POST request and save the response
    send_post_request(longitude, latitude)