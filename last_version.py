#in this project we will take the participants, the meeting context and the meeting goal

#this application will help us get a brief and to know which points of interest will be interesting to cover in the meeting
#based on the participants background information...etc and the goal of the meeting


#this is a sequential process, given that each agent will make it's task sequentially
#there are another processes like hierachical whereas an agent on the top can assign tasks to other agents that he decides along the way


from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import requests

from twitter_data_retrieval import get_user_data
import json
from dotenv import load_dotenv

load_dotenv()

import os

# TODO: Import and initialize your custom tools here

from crewai_tools import BaseTool
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from twitter_data_retrieval import get_user_data
from music_gen import run_generation

# Retrieve the user data

# user_name = "tszzl"
# user_name = "jvboid"


# docs_researcher
from agents_v1 import  bio_researcher, reporter, prompt_enhancer, suno_runner
from tools import SunoAPI
# Define agents with more specific roles


from images_explainers import explain_pfp_banner


def run_agents(user_name="manu__martinm"):
    """
    returns public url of the generated audio
    """
    

    user_json, images = get_user_data(user_name=user_name)



    pfp_report, banner_report = explain_pfp_banner(user_name=user_name)

    print(pfp_report)

    task_bio_research = Task(
        description=f"""Combine this json array about info of a twitter user profile (bio, tweets...etc) and these two reports about his/her profile picture and banner picture
        
        user's details & tweets JSON: {user_json},
        
        pfp report: {pfp_report},
        
        banner_report: {banner_report}
        """,
        agent=bio_researcher,
        expected_output="Bullet-point list of humorous observations about the user's Twitter behavior and personality",
        async_execution=False,

    )


    task_combining_report = Task(
        description="""
        Synthesize the analyses of the bio, profile picture, and banner into a hilarious Twitter user profile. Your report should:
        - Highlight the most absurd or exaggerated aspects of the user's online presence
        - Create funny connections between their tweets, profile picture, and banner
        - Suggest a "Twitter personality type" for the user (e.g., "The Hashtag Abuser", "The Accidental Philosopher")
        - Include a mock "Twitter bio" that exaggerates their actual traits
        - Propose a funny "claim to fame" based on their Twitter behavior
        
        Structure your report as a series of tweet-length observations, perfect for adaptation into song lyrics.
        """,
        agent=reporter,
        expected_output="A collection of tweet-length, humorous observations about the user, ready for lyrical adaptation",
            async_execution=False,

    )

    task_prompt_enhancer = Task(
        description="""
        Transform the humorous Twitter profile into song lyrics and a music style description. Your output should include:
        
        1. Lyrics:
        - A catchy chorus that encapsulates the user's Twitter essence
        - Verses that elaborate on specific funny observations
        - A bridge that introduces a surprising twist or self-awareness about their Twitter behavior
        
        2. Music Style:
        - Choose a genre that ironically fits the user's online persona (e.g., a power ballad for someone who only tweets about coding)
        - Suggest specific musical elements that match Twitter behaviors (e.g., autotune for someone who overuses emojis)
        
        3. Song Title:
        - Create a title that's both a play on words and related to the user's Twitter presence
        
        4. Tags:
        - Include relevant musical style tags and humorous descriptors
        
        Provide the output in this JSON format:
        {
        "prompt": "[Verse 1] ... lyrics \n\n [Chorus] ... lyrics \n\n [Verse 2] ... lyrics \n\n [Bridge] ... lyrics \n\n [Chorus] ... lyrics",
        "tags": "chosen musical style, funny descriptors",
        "title": "Clever song title",
        "make_instrumental": false,
        "wait_audio": false
        }
        """,
        agent=prompt_enhancer,
        expected_output="JSON object containing humorous song lyrics, style tags, and a clever title derived from the Twitter profile analysis with the specified attributes,",
            async_execution=False,

    )
    task_song_gen = Task(
        description="""It will run the endpoint of the Suno AI generation model, giving as parameter.
        
        """,
        tools=[SunoAPI(result_as_answer=True)],
        agent=suno_runner,
        expected_output="The generated audio link string that you got printed when using the tool.",
            async_execution=False,

    )

    # Create and execute the Crew
    crew = Crew(
        agents=[bio_researcher, reporter, prompt_enhancer, suno_runner],
        tasks=[task_bio_research, task_combining_report, task_prompt_enhancer, task_song_gen],
        verbose=1 # Increased verbosity for more detailed logging
    )

    result = crew.kickoff()
    print(result)


    # response = requests.get(result)

    # Check if the request was successful
    return result