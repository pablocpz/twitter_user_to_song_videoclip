<<<<<<< HEAD
# Ready Twitter to Karaoke

## Overview
This repository contains a Twitter bot that analyzes Twitter user profiles and generates humorous song lyrics based on their tweets and profile information. The bot utilizes various APIs to retrieve user data, process it, and generate audio content.

## Features
- Retrieve Twitter user data including bio, profile picture, and tweets.
- Analyze user data to create humorous observations and song lyrics.
- Generate audio files from the created lyrics using the Suno AI model.
- Post generated content back to Twitter.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ready-twitter-to-karaoke.git
   cd ready-twitter-to-karaoke
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```plaintext
   SOCIALDATA_API_KEY=your_socialdata_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage
1. Run the bot:
   ```bash
   python src/backend/botapp.py
   ```

2. The bot will start monitoring replies to a specific tweet and generate content based on user interactions.

## Code Structure
- `src/backend/`: Contains the main application logic.
- `src/backend/last_version.py`: Handles the processing of user data and interaction with the AI model.
- `src/backend/botapp.py`: Manages the Twitter bot functionality.
- `src/backend/tweet_replies.py`: Retrieves replies to a specific tweet.
- `src/backend/twitter_data_retrieval.py`: Fetches user data from Twitter.
- `src/backend/music_gen.py`: Interfaces with the Suno AI model for audio generation.
- `src/backend/config.py`: Contains API keys and configuration settings.
=======
# ready-twitter-to-karaoke


Run the botapp.py main file.
Ensure you already created a `credentials.ini` file in the root dir, looking as follows:
```bash
Authentication]
access_token = XXXXXXXXX
app_key = XXXXXXXXXX
app_secret = XXXXXXXXXXXX
refresh_token = XXXXXXXXXX
```
These should be the **dropbox api keys**
>>>>>>> 64fabfdf463302d4183d89a31b733898304f01d0
