import requests
import logging
import json
import re
import urllib.parse
import random

DUCKDUCKGO_IMAGE_SEARCH_URL = "https://duckduckgo.com"
DUCKDUCKGO_IMAGE_API_URL = "https://duckduckgo.com/i.js"

# List of rotating user-agents to mimic real browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
]

def fetch_image_url(description):
    """
    Fetches an image URL based on the description using DuckDuckGo's public image search.
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),  # Rotate User-Agent
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://duckduckgo.com/",
        "DNT": "1",  # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

    try:
        # Get the vqd token required for the image search
        logging.info(f"Searching DuckDuckGo for: {description}")
        init_response = requests.get(f"{DUCKDUCKGO_IMAGE_SEARCH_URL}/?q={urllib.parse.quote(description)}&iax=images&ia=images", headers=headers)
        init_response.raise_for_status()

        # Extract the vqd token from the HTML source using regex
        token_match = re.search(r'vqd=([\d-]+)&', init_response.text)
        if not token_match:
            logging.error("Failed to extract token for DuckDuckGo image search.")
            return None
        
        vqd_token = token_match.group(1)
        logging.info(f"Extracted token: {vqd_token}")

        # Use the token to perform the image search
        params = {
            "q": description,
            "iax": "images",
            "ia": "images",
            "vqd": vqd_token,
            "o": "json"
        }
        search_response = requests.get(DUCKDUCKGO_IMAGE_API_URL, headers=headers, params=params)
        search_response.raise_for_status()

        # Parse the JSON response and extract the first direct image URL
        search_results = search_response.json()
        if search_results.get("results"):
            image_url = search_results["results"][0]["image"]
            logging.info(f"Found direct image URL: {image_url}")
            return image_url
        else:
            logging.error("No image found.")
            return None
    except Exception as e:
        logging.error(f"Error fetching image from DuckDuckGo: {e}")
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

