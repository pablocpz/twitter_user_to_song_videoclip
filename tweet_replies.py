from dotenv import load_dotenv
import os
import requests
load_dotenv()
bearer_token = os.getenv("SOCIALDATA_API_KEY")


def get_replies():
    
    """
    It retrieves the comments on my original tweet.
    
    It should run the prediction karaoke for the quoted user on each reply
    
    We should store the users who already replied in a database (their usernames)
    
    #we could run this async every 1 min
    
    
    output
    
    list for each reply in the tweet:
    
    {
    'reply_id': 
    'reply_date': '2024-10-06T19:25:14.000000Z',
    'target_username': 'vinijr'}
    
    """
    # query = "from%3Aelonmusk&type=Latest"
    tweet_id = "1843000399915274691"

    # query = "conversation_id:"
    url = "https://api.socialdata.tools/twitter/search?query=conversation_id:1843000399915274691"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    # print(response.json())

    replies = response.json()["tweets"]

    replies_list = []
    
    
    for reply in replies:
        #print reply's content
        
        #it should be @user_to_karaoke @username
        #or whathever staring with @user_to_karaoke do it for @username :))
        
        # content = reply["full_text"]
        
        # original_user = reply[""]
        # created_at = reply["tweet_created_at"]
        
        
        #we can simply get the user mentioned (supposing it only quoutes one at a time)
        
        if reply["user"]["screen_name"] != "user_to_karaoke":
            quoted_users = reply["entities"]["user_mentions"]
            
            target_user = [user["screen_name"] for user in quoted_users if len(quoted_users)>=0][-1]
            
            
            
            reply_date = reply["tweet_created_at"]
            reply_id = reply["id_str"]
            
            replies_list.append({
                "reply_id" : reply_id,
                "reply_date" : reply_date,
                "target_username" : target_user
        })
        
        
        
    print(replies_list)
    # print(replies_list)
    return replies_list
        
# get_replies()