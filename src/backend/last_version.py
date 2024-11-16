# This script processes Twitter user data to generate humorous song lyrics based on their profile and tweets.

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import requests
from twitter_data_retrieval import get_user_data
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define the main function to run agents for a given Twitter user
def run_agents(user_name="manu__martinm"):
    """
    Returns public URL of the generated audio based on the user's Twitter profile.
    """
    
    # Retrieve user data and images
    user_json, images = get_user_data(user_name=user_name)
    pfp_report, banner_report = explain_pfp_banner(user_name=user_name)

    # Create tasks for different agents
    task_bio_research = Task(
        description=f"""Combine this json array about info of a twitter user profile (bio, tweets...etc) and these two reports about his/her profile picture and banner picture
        user's details & tweets JSON: {user_json},
        pfp report: {pfp_report},
        banner_report: {banner_report}""",
        agent=bio_researcher,
        expected_output="Bullet-point list of humorous observations about the user's Twitter behavior and personality",
        async_execution=False,
    )

    task_combining_report = Task(
        description="""Synthesize the analyses of the bio, profile picture, and banner into a hilarious Twitter user profile. Your report should:
        - Highlight the most absurd or exaggerated aspects of the user's online presence
        - Create funny connections between their tweets, profile picture, and banner
        - Suggest a "Twitter personality type" for the user
        - Include a mock "Twitter bio" that exaggerates their actual traits
        - Propose a funny "claim to fame" based on their Twitter behavior""",
        agent=reporter,
        expected_output="A collection of tweet-length, humorous observations about the user, ready for lyrical adaptation",
        async_execution=False,
    )

    task_prompt_enhancer = Task(
        description="""Transform the humorous Twitter profile into song lyrics and a music style description. Your output should include:
        1. Lyrics: A catchy chorus, verses, and a bridge
        2. Music Style: Choose a genre that ironically fits the user's online persona
        3. Song Title: A clever title related to the user's Twitter presence
        4. Tags: Relevant musical style tags and humorous descriptors""",
        agent=prompt_enhancer,
        expected_output="JSON object containing humorous song lyrics, style tags, and a clever title derived from the Twitter profile analysis.",
        async_execution=False,
    )

    task_song_gen = Task(
        description="""Run the endpoint of the Suno AI generation model, giving as parameter.""",
        tools=[SunoAPI(result_as_answer=True)],
        agent=suno_runner,
        expected_output="The generated audio link string that you got printed when using the tool.",
        async_execution=False,
    )

    # Create and execute the Crew
    crew = Crew(
        agents=[bio_researcher, reporter, prompt_enhancer, suno_runner],
        tasks=[task_bio_research, task_combining_report, task_prompt_enhancer, task_song_gen],
        verbose=1  # Increased verbosity for more detailed logging
    )

    result = crew.kickoff()
    print(result)
    return result 