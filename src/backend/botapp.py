# This script manages the Twitter bot functionality, including tweeting and replying to users.

import logging
import tweepy
import time
import datetime
import pandas as pd
from config import api_key, api_key_secret, access_token, access_token_secret, bearer_token
from tweet_replies import get_replies
from last_version import run_agents

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Constants for tweet limits
MAX_TWEETS_PER_DAY = 48
MAX_TWEETS_PER_MONTH = 1500
MAX_REST_DURATION_SECONDS = 43400

def load_data():
    """Load data from a CSV file."""
    filename = "frasesbd.csv"
    df = pd.read_csv(filename)
    return df

def format_tweet(frase, autor):
    """Format the tweet message."""
    return f'"{frase}" -{autor}'

def tweet_message(client, message, tweet_id):
    """Send a tweet message."""
    try:
        client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)
        client.create_tweet(text=message, in_reply_to_tweet_id=tweet_id)
        logger.info('Tweeted successfully: {}'.format(message))
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
    """Reply to a tweet."""
    try:
        client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)
        tweet_id = '1843000399915274691'
        client.create_tweet(text=message, in_reply_to_tweet_id=tweet_id, reply_settings="mentionedUsers")
        logger.info('Tweeted successfully: {}'.format(message))
    except tweepy.errors.TweepyException as e:
        if "limit" in str(e):
            logger.info('Tweet limit reached. Sleeping for 3 hours')
            time.sleep(3 * 60 * 60)
        else:
            logger.error(e)
            raise e
    except Exception as e:
        logger.error('An error occurred while tweeting: {}'.format(e))

def check_tweet_limit(daily_tweet_count):
    """Check if the daily tweet limit has been reached."""
    return daily_tweet_count >= MAX_TWEETS_PER_DAY

def main(interval):
    """Main function to run the bot."""
    logger.info('Starting the script')
    client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
    daily_tweet_count = 0
    monthly_tweet_count = 0
    current_month = datetime.datetime.today().month
    last_month = current_month

    while True:
        current_execution_time = datetime.datetime.now(datetime.timezone.utc)
        replies_list = get_replies()

        # Process the filtered replies
        target_usernames = [reply["target_username"] for reply in replies_list]
        author_ids = [reply["reply_id"] for reply in replies_list]

        for idx, input_username in enumerate(target_usernames):
            logger.info(input_username)
            logger.info(author_ids[idx])
            generated_url = run_agents(user_name=input_username)
            public_url = run(generated_url)
            tweet_message(client, f"🍳 Yoo, here you got your public song URL: {public_url}", tweet_id=author_ids[idx])
            time.sleep(random.randint(2, 3))
            daily_tweet_count += 1
            monthly_tweet_count += 1

        time.sleep(interval)

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
                time.sleep(60 * 60)  # Sleep for an hour and check the month again

if __name__ == '__main__':
    interval = 30  # every 30 secs it will run everything
    main(interval) 