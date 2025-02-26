import logging
import requests
import os

# Google Custom Search JSON API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def is_valid_image_url(url, min_width=100):
    """
    Checks if the image URL is valid and publicly accessible.
    Filters out SVGs, decorative images, and thumbnails smaller than min_width.
    """
    # Filter out SVGs and other non-suitable images
    if (url.endswith(".svg") or                 
        "placeholder" in url):                
        logging.warning(f"Filtered out non-content image: {url}")
        return False

    # Check if the URL is publicly accessible
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            logging.info(f"Image URL is publicly accessible: {url}")
            return True
        else:
            logging.warning(f"Image URL returned non-200 status: {url}")
            return False
    except Exception as e:
        logging.error(f"Error checking image URL: {url}, Exception: {e}")
        return False

def fetch_image_url(description):
    """
    Fetches an image URL based on the description using Google Custom Search JSON API.
    """
    try:
        # Prepare API request
        search_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'q': description,
            'cx': SEARCH_ENGINE_ID,
            'key': GOOGLE_API_KEY,
            'searchType': 'image',
            'num': 3  # Number of images to return
        }
        
        # Make the API request
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        search_results = response.json()
        if 'items' not in search_results:
            logging.error(f"No image found for: {description}")
            return None

        # Check each image URL
        for item in search_results['items']:
            image_url = item['link']
            if is_valid_image_url(image_url):
                logging.info(f"Found valid image URL: {image_url}")
                return image_url
        
        # If no valid image is found, return None
        logging.error("No valid image found using Google Custom Search.")
        return None
    except Exception as e:
        logging.error(f"Error fetching image from Google Custom Search: {e}")
        return None


def download_image(image_url):
    """
    Downloads the image from the given URL and returns the binary data.
    """
    try:
        logging.info(f"Attempting to download image from: {image_url}")
        response = requests.get(image_url, stream=True)
        logging.info(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Image downloaded successfully.")
            return response.content
        else:
            logging.error(f"Non-200 response received: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None

