# This module defines tools for interacting with external APIs, specifically for music generation.

from crewai_tools import BaseTool
import requests
from music_gen import run_generation
import json 

class SunoAPI(BaseTool):
    name: str = "SUNO Music Gen API tool"
    description: str = "It runs the music generation endpoint, vital for the last step of the workflow. It will retrieve a public URL of the generated song"

    def _run(self, payload: str) -> str:
        """
        Runs the music generation API with the provided payload.
        Returns the URL of the generated song.
        """
        song_url = run_generation(payload=payload)
        response = requests.get(song_url)

        # Check if the request was successful
        if response.status_code == 200:
            return song_url
        else:
            print("Failed to download the file. Status code:", response.status_code)
            return None 