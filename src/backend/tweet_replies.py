# This module retrieves replies to a specific tweet and extracts relevant user information.

from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()
bearer_token = os.getenv("SOCIALDATA_API_KEY")

def get_replies():
    """
    Retrieves the comments on a specific tweet.
    Returns a list of replies with their IDs, dates, and target usernames.
    """
    tweet_id = "1843000399915274691"
    url = f"https://api.socialdata.tools/twitter/search?query=conversation_id:{tweet_id}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    replies = response.json()["tweets"]

    replies_list = []
    
    for reply in replies:
        if reply["user"]["screen_name"] != "user_to_karaoke":
            quoted_users = reply["entities"]["user_mentions"]
            target_user = [user["screen_name"] for user in quoted_users if len(quoted_users) >= 0][-1]
            reply_date = reply["tweet_created_at"]
            reply_id = reply["id_str"]
            
            replies_list.append({
                "reply_id": reply_id,
                "reply_date": reply_date,
                "target_username": target_user
            })
    
    return replies_list 