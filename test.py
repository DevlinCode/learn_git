import os
import requests
from serpapi import GoogleSearch

# Set up directories for saving images
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_image(url, file_name):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"Could not save {file_name}: {e}")

# Configuration
def download_images(search_query, api_key, output_dir, num_images=500):
    create_dir(output_dir)
    search = GoogleSearch({
        "q": search_query,
        "tbm": "isch",
        "num": 100,  # Fetch 100 at a time
        "api_key": api_key
    })
    
    images_downloaded = 0
    while images_downloaded < num_images:
        results = search.get_dict()
        for image in results.get("images_results", []):
            if images_downloaded >= num_images:
                break
            
            image_url = image.get("original")
            if image_url:
                save_image(image_url, f"{output_dir}/image_{images_downloaded+1}.jpg")
                print(f"Downloaded: image_{images_downloaded+1}.jpg")
                images_downloaded += 1
        
        # Go to the next page
        if "next" in results.get("serpapi_pagination", {}):
            search.params_dict["start"] = results["serpapi_pagination"]["next"]
        else:
            break

# Parameters
API_KEY = "your_serpapi_api_key"
SEARCH_QUERY = "cute puppies"
OUTPUT_DIR = "images"

download_images(SEARCH_QUERY, API_KEY, OUTPUT_DIR, num_images=500)
