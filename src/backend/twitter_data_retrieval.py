# This module retrieves user data and tweets from Twitter.

import requests
from io import BytesIO
import base64
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
bearer_token = os.getenv("SOCIALDATA_API_KEY")

def get_tweets(user_id):
    """
    Returns the latest tweets and replies for a given user ID.
    """
    url = f"https://api.socialdata.tools/twitter/user/{user_id}/tweets-and-replies"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    tweets = []
    while True:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            tweets.extend(data.get("tweets", []))
            
            # Check if we have collected enough tweets
            if len(tweets) >= 20:
                break
            
            # Check if there is a next_cursor
            next_cursor = data.get("next_cursor")
            if next_cursor:
                url = f"https://api.socialdata.tools/twitter/user/{user_id}/tweets-and-replies?cursor={next_cursor}"
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            break

    return tweets

def get_user_data(user_name):
    """
    Retrieves a user's bio details, profile picture, banner, and tweets.
    Returns a dictionary with user data and a list of images in base64 encoding.
    """
    url = f"https://api.socialdata.tools/twitter/user/{user_name}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Extract user information
        user_data = {
            "user_bio": data.get("description"),
            "user_id": data.get("id"),
            "user_creation": data.get("created_at"),
            "user_verified": data.get("verified"),
            "user_followers_count": data.get("followers_count"),
            "user_location": data.get("location"),
            "user_dm": None if data.get("can_dm") == "null" else data.get("can_dm"),
            "user_following_count": data.get("friends_count"),
            "user_privated": data.get("protected")
        }
        
        # Retrieve the latest tweets
        tweets = get_tweets(user_id=user_data["user_id"])
        user_data["tweets"] = tweets
        
        # Download and encode profile and banner images
        def download_image(url):
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
                return base64_image
            else:
                print(f"Error downloading image: {response.status_code}")
                return None

        # Download profile image
        if data.get('profile_image_url_https'):
            user_pfp_base64 = download_image(data.get('profile_image_url_https'))
        
        # Download banner image
        user_banner_url = data.get('profile_banner_url')
        if user_banner_url:
            user_banner_url += "/1500x500"  # Add banner size
            banner_image_base64 = download_image(user_banner_url)
            if banner_image_base64:
                user_banner_base64 = banner_image_base64
        else:
            user_banner_base64 = None

        return user_data, [user_pfp_base64, user_banner_base64]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None 