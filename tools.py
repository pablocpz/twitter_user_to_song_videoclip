from crewai_tools import BaseTool
import requests
from music_gen import run_generation
import json 

class SunoAPI(BaseTool):
    name: str = "SUNO Music Gen API tool"
    description: str = "It runs the music generation endpoint, vital for the last step of the workflow. It will retrieve a public URL of the generated song"

    def _run(self, payload:str) -> str:
        # Your tool's logic here
        
        # print(payload)
        
            
        song_url = run_generation(payload=payload)
            
        response = requests.get(song_url)

        # Check if the request was successful
        if response.status_code == 200:
            print("sucessful1")
            # # Get the content type to infer the file extension
            # content_type = response.headers.get('Content-Type')
            # if 'audio' in content_type:
            #     print("audio:")
            #     file_extension = content_type.split('/')[1]
            #     filename = f'downloaded_song.{file_extension}'
            # else:
            #     filename = 'downloaded_song.mp3'

            # # Write the content to a local file
            # with open(filename, 'wb') as file:
            #     file.write(response.content)
            # print(f"Download complete. File saved as {filename}.")
        else:
            print("Failed to download the file. Status code:", response.status_code)
        return song_url
    
    
# from langchain.utilities import SerpAPIWrapper
# search = SerpAPIWrapper()    
# import requests
# from langchain.tools import Tool


# from langchain.tools import BaseTool
# from bs4 import BeautifulSoup

# SearchSocialDataAPI = Tool(
#     name="SocialData API Documentation Search",
#     func=search.run,
#     description="Searches the web for SocialData API documentation and information about tweet retrieval."
# )

# class SearchSocialDataAPI(BaseTool):
#     name = "SocialData API Reference Docs"
#     description = "Searches the official API docs of the SocialData API for information about tweet retrieval."

#     def _run(self, query: str) -> str:
#         # URL of the SocialData API documentation
#         base_url = "https://socialdata.gitbook.io/docs/"
#         search_url = f"{base_url}search?q={query}"

#         try:
#             response = requests.get(search_url)
#             response.raise_for_status()

#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Find search results
#             results = soup.find_all('div', class_='css-1qlsa13')

#             if not results:
#                 return "No results found in the SocialData API documentation."

#             # Process and format the results
#             formatted_results = []
#             for result in results[:3]:  # Limit to top 3 results
#                 title = result.find('div', class_='css-1l9l9x8').text.strip()
#                 snippet = result.find('div', class_='css-1fu1vtx').text.strip()
#                 link = base_url + result.find('a')['href']
#                 formatted_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")

#             return "\n".join(formatted_results)

#         except requests.RequestException as e:
#             return f"An error occurred while searching the SocialData API documentation: {str(e)}"

#     def _arun(self, query: str):
#         # This tool does not support async execution
#         raise NotImplementedError("This tool does not support async execution")