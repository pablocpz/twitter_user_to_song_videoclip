import requests
import json
import base64
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()

def explain_pfp_banner(user_name):
    # Twitter user URL
    url = f"https://api.socialdata.tools/twitter/user/{user_name}"

    # Headers for the request
    headers = {
        "Authorization": os.getenv("SOCIALDATA_API_KEY"),
        "Accept": "application/json"
    }

    # Make the request to get user data
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        exit()

    # Get profile image URL and banner URL
    profile_image_url = data['profile_image_url_https']
    banner_url = data.get("profile_banner_url")

    if banner_url:
        banner_url += "/1500x500"

    # Function to encode an image from a URL
    def encode_image_from_url(image_url, new_size=(224, 224)):
        response = requests.get(image_url)
        if response.status_code == 200:
            with Image.open(io.BytesIO(response.content)) as img:
                # Resize the image
                img = img.resize(new_size, Image.LANCZOS)
                # Convert to RGB if it's not
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Save to a bytes buffer
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
        else:
            print(f"Error fetching image: {response.status_code}")
            return None

    # Get base64 encodings for profile image and banner
    base64_profile_image = encode_image_from_url(profile_image_url)
    base64_banner_image = encode_image_from_url(banner_url) if banner_url else None

    # OpenAI API Key

    # Prepare the headers for OpenAI API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    # Prepare the payload
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Fully describe this profile image"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_profile_image}",
                        "detail": "high"
                    }
                }
            ]
        }
    ]


    payload = {
        "model": "gpt-4o",
        "messages": messages,
        # "max_tokens": 300
    }

    # Send request to OpenAI API
    response_pfp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json().get('choices', [{}])[0].get('message', {}).get('content', '')

    # Print the response
    # print(response.json())



    # If the banner exists, add it to the messages
    if base64_banner_image:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Fully describe this banner image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_banner_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
        
    payload = {
        "model": "gpt-4o",
        "messages": messages,
        # "max_tokens": 300
    } # SIN LIMIT TOKENS DE MOMENTO

    response_banner = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json().get('choices', [{}])[0].get('message', {}).get('content', '')

    
    
    return response_pfp, response_banner


# print(explain_pfp_banner("tszzl"))