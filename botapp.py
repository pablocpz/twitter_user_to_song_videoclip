import logging
import tweepy
import time
import datetime
import pandas as pd
from config import api_key, api_key_secret, access_token, access_token_secret, bearer_token


from tweet_replies import get_replies
from last_version import run_agents

# from dotenv import load_dotenv
# import os
# import requests
# load_dotenv()
# bearer_token = os.getenv("SOCIALDATA_API_KEY")


MAX_TWEETS_PER_DAY = 48
MAX_TWEETS_PER_MONTH = 1500
MAX_REST_DURATION_SECONDS = 43400
# MAX_INTERVAL = 5.7 * 60 * 60 

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

#Disclaimer: I don't document simple functions, too lazy.
def load_data():
    # Define the filename with double backslashes for Windows
    filename = "frasesbd.csv"

    # Load the XLSX file into a DataFrame
    df = pd.read_csv(filename)
    return df

def format_tweet(frase, autor):
    # Format the tweet as "frase" -autor
    return f'"{frase}" -{autor}'


def tweet_message(client, message, tweet_id):
    """
    User rate limit (User context):
    200 requests per 15-minute window per each authenticated user
    
    
    == 13 tweets / minute = 5 tweets each 30 secs
    """
    try:
        '''
        Use the v2 endpoint to create a tweet. By doing this, you guarantee
        the script won't get a timeout error due to it eventually waiting on 
        time.sleep() for one reason or another, which one could get by calling 
        tweepy.Client() on main().
        '''

        client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)
        client.create_tweet(text=message,
                            in_reply_to_tweet_id=tweet_id)
        
        logger.info('Tweeted successfully: {}'.format(message))

        

    #Handling common (and uncommon!) errors.    
    except tweepy.errors.TweepyException as e:
        if "limit" in str(e):
            logger.info('Tweet limit reached. Sleeping for 3 hours')
            time.sleep(3 * 60 * 60)
        else:
            logger.error(e)
            raise e
    except Exception as e:
        logger.error('An error occurred while tweeting: {}'.format(e))
        
        
        

def reply_tweet(client, message):
    try:

        client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)
        
        #retrieve tweets where we are mentioned    
        name = 'user_to_karaoke'
        tweet_id = '1843000399915274691'

    
        
        # client.create_tweet(text=message,
        #                     in_reply_to_tweet_id=tweet_id)
        client.create_tweet(text=message,
                            in_reply_to_tweet_id=tweet_id,
                            reply_settings="mentionedUsers")
        logger.info('Tweeted successfully: {}'.format(message))

        

    #Handling common (and uncommon!) errors.    
    except tweepy.errors.TweepyException as e:
        if "limit" in str(e):
            logger.info('Tweet limit reached. Sleeping for 3 hours')
            time.sleep(3 * 60 * 60)
        else:
            logger.error(e)
            raise e
    except Exception as e:
        logger.error('An error occurred while tweeting: {}'.format(e))



# def get_mentioned_tweets(client):

#     try:
#         client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)

#         # client.create_tweet(text=message)
#         # logger.info('Tweeted successfully: {}'.format(message))
        
#         url = "https://api.socialdata.tools/twitter/user/user_to_karaoke"
#         headers = {
#             "Authorization": f"Bearer {bearer_token}",
#             "Accept": "application/json"
#         }
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:
#             data = response.json()
        
#         user_id = str(data["id"])
        
#         logger.info(user_id)
#         print("................")
#         print(type(user_id))
#         mentioned_tweets = client.get_users_mentions(id=user_id)
        
#         logger.info(mentioned_tweets)

#     #Handling common (and uncommon!) errors.    
#     except tweepy.errors.TweepyException as e:
#         if "limit" in str(e):
#             logger.info('Tweet limit reached. Sleeping for 3 hours')
#             time.sleep(3 * 60 * 60)
#         else:
#             logger.error(e)
#             raise e
#     except Exception as e:
#         logger.error('An error occurred while tweeting: {}'.format(e))




def check_tweet_limit(daily_tweet_count):
    return daily_tweet_count >= MAX_TWEETS_PER_DAY

import datetime
import requests
import time
last_execution_time = None
import random


from dropbox_api import run

def main(interval):
    global last_execution_time

    # Start the script
    logger.info('Starting the script')
    
    '''
    Create a Tweepy client. Not strictly necessary here since tweet_message() also makes a call every tweet.
    Just to be safe and not have any issues later down the road if one adds new features to main().
    '''
    client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)

    # df = load_data()

    # # Initialize the daily and monthly tweet count
    daily_tweet_count = 0
    monthly_tweet_count = 0
    current_month = datetime.datetime.today().month
    last_month = current_month
    #---- por defecto (arriba uncomment)
    
    
    # reply_tweet(client=client, message="wooow, i did it, beep, boop!")
    
    
    # replies_list = get_replies()
    
    # target_usernames = []
    # for reply in replies_list:
    #     target_usernames.append(reply["target_username"])
    #     #we don't need the date and author since we can just 
        #compare the current time, against the last time we ran get_replies()
        
    while True:
        # Current execution time
        # current_execution_time = datetime.datetime.utcnow()
        current_execution_time = datetime.datetime.now(datetime.timezone.utc)
        
        # Get replies
        replies_list = get_replies()

        # Filter replies based on the last execution time
        if last_execution_time:
            logger.info(f"Filtering replies since last execution at {last_execution_time}")
            filtered_replies = [
                reply for reply in replies_list
                if datetime.datetime.strptime(reply["reply_date"], "%Y-%m-%dT%H:%M:%S.%fZ") > last_execution_time
            ]
        else:
            filtered_replies = replies_list  # If this is the first run, no filtering

        # Process the filtered replies
        target_usernames = [reply["target_username"] for reply in filtered_replies]
        author_ids = [reply["reply_id"] for reply in filtered_replies]
        
        #we do the AI here   
        
        # n_predictions = 0 #we can do 6 predictions as much (every 30 secs)
        
        for idx, input_username in enumerate(target_usernames):
            """
            iterating through the current input usernames
            
            we'll run the inference here
            """
            
            # Check if the request was successful
            logger.info(input_username)
            logger.info(author_ids[idx])
            logger.info("-..............")
            generated_url = run_agents(user_name=input_username)
            
            # response = requests.get(generated_url, stream=True)

            # if response.status_code == 200:
            #     with open("downloaded_song.mp3", 'wb') as f:
            #         for chunk in response.iter_content(1024):
            #             f.write(chunk)
            #     print(f"File downloaded successfully from {generated_url}")
            # else:
            #     print(f"Failed to download file from {generated_url}, status code: {response.status_code}")
            
            public_url = run(generated_url)
            
            
            
            print(f"Tweeting")  # DEBUG what's being tweeted

            tweet_message(client, f"🍳 Yoo, here you got your public song URL: {public_url}", tweet_id=author_ids[idx])
            
            time.sleep(random.randint(2,3))
            #we'll wait some secs between each scrapped reply
            
            daily_tweet_count += 1
            monthly_tweet_count += 1
            

        time.sleep(interval) #we will check for new replies every 30 secs

        if check_tweet_limit(daily_tweet_count):
            logger.info('Tweet limit for the day reached. Resting for {} seconds'.format(MAX_REST_DURATION_SECONDS))
            time.sleep(MAX_REST_DURATION_SECONDS)
            daily_tweet_count = 0

        # Check if it's a new month and reset the monthly count
        current_month = datetime.datetime.today().month
        if current_month != last_month:
            logger.info('New month started. Resetting monthly tweet count.')
            last_month = current_month
            monthly_tweet_count = 0

        if monthly_tweet_count >= MAX_TWEETS_PER_MONTH:
            logger.info('Monthly tweet limit reached. Waiting for the new month.')
            while current_month == last_month:
                time.sleep(60*60)  # Sleep for an hour and check the month again, since, with current settings, it's highly unlikely it will ever hit it

    
        
        
        
        
        
        
        
        logger.info(f"Target usernames: {target_usernames}")

        # Update last_execution_time with the current execution time
        last_execution_time = current_execution_time

        # Sleep for the specified interval (30 seconds in this case)
        logger.info(f"Waiting for {interval} seconds before next execution...")
        time.sleep(interval)   
    
    
    # for index, row in df.iterrows():
    #     frase = row['frase']
    #     autor = row['autor']
    #     tweet = format_tweet(frase, autor)

    #     print(f"Tweeting: {tweet}")  # DEBUG what's being tweeted

    #     tweet_message(client, tweet)
        
    #     daily_tweet_count += 1
    #     monthly_tweet_count += 1
        

    #     time.sleep(interval)

    #     if check_tweet_limit(daily_tweet_count):
    #         logger.info('Tweet limit for the day reached. Resting for {} seconds'.format(MAX_REST_DURATION_SECONDS))
    #         time.sleep(MAX_REST_DURATION_SECONDS)
    #         daily_tweet_count = 0

    #     # Check if it's a new month and reset the monthly count
    #     current_month = datetime.datetime.today().month
    #     if current_month != last_month:
    #         logger.info('New month started. Resetting monthly tweet count.')
    #         last_month = current_month
    #         monthly_tweet_count = 0

    #     if monthly_tweet_count >= MAX_TWEETS_PER_MONTH:
    #         logger.info('Monthly tweet limit reached. Waiting for the new month.')
    #         while current_month == last_month:
    #             time.sleep(60*60)  # Sleep for an hour and check the month again, since, with current settings, it's highly unlikely it will ever hit it

       
    # logger.info('Script finished')

if __name__ == '__main__':
    
    # interval = MAX_INTERVAL
    interval = 30 #every 30 secs it will run everything ()

    main(interval)
