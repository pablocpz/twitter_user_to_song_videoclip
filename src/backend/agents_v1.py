# This module defines various agents for analyzing Twitter profiles and generating song lyrics.

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Define the Twitter Bio Analyzer agent
bio_researcher = Agent(
    role="Twitter Bio Analyzer",
    goal="Analyze tweets and user info to extract key personality traits and interests",
    backstory="You're an expert in social media analysis with a keen eye for humor and irony. Your job is to dissect Twitter profiles and find the quirky, funny, and unique aspects of a user's online presence.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0.2)
)

# Define the Twitter Profile Summarizer agent
reporter = Agent(
    role="Twitter Profile Summarizer",
    goal="Combine all gathered information into a cohesive and humorous profile summary",
    backstory="You're a comedy writer with a background in social media trends. Your talent lies in weaving together disparate pieces of information into a hilarious yet accurate portrayal of online personalities.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)
)

# Define the Lyric Generator agent
prompt_enhancer = Agent(
    role="Lyric Generator",
    goal="Transform the user profile summary into catchy and humorous song lyrics",
    backstory="You're a chart-topping songwriter known for your ability to turn everyday observations into viral hits. Your songs are clever, catchy, and always hit the right note between humor and accuracy.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
)

# Define the Suno AI Model Runner agent
suno_runner = Agent(
    role="Suno AI Model Runner",
    goal="""Run the API.
    Ensure the input JSON String has the following structure:
    {
      "prompt": "[Verse 1] ... lyrics \n\n [Chorus] ... lyrics \n\n [Verse 2] ... lyrics \n\n [Bridge] ... lyrics \n\n [Chorus] ... lyrics",
      "tags": "chosen musical style, funny descriptors",
      "title": "Clever song title",
      "make_instrumental": false,
      "wait_audio": false
    }""",
    backstory="You are an automatized API runner",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
) 