
import time
import requests
import json

# Replace your Vercel domain
# base_url = 'https://suno-api-eosin-nu.vercel.app/api/'
base_url = 'https://suno-api-pi-seven.vercel.app/api'


def custom_generate_audio(payload):
    url = f"{base_url}/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

def run_generation(payload:str):
    """
    It returns the first generated song's URL given the payload JSON string object
    """
    
    payload = json.loads(payload)
    # # Payload for custom audio generation
    # payload = {
    #     "prompt": """[Verse 1]\nCruel flames of war engulf this land\n
    #     Battlefields filled with death and dread\n
    #     Innocent souls in darkness, they rest\n
    #     My heart trembles in this silent test\n
    #     \n[Verse 2]\nPeople weep for loved ones lost\nBattered bodies bear the cost\nSeeking peace and hope once known\nOur grief transforms to hearts of stone\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Bridge]\nThrough the ashes, we will rise\nHand in hand, towards peaceful skies\nNo more sorrow, no more pain\nTogether, we'll break these chains\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Outro]\nIn unity, our strength will grow\nA brighter future, we'll soon know\nFrom the ruins, hope will spring\nA new dawn, we'll together bring""",
        
        
    #     "tags": "pop metal male melancholic",
        
    #     "title": "Silent Battlefield",
        
    #     "make_instrumental": False, #if we don't want vocals , so just instruments 
        
    #     "wait_audio": False #it will give us the status of the generation so we can check
    # }
    # it works :))

    # Generate audio using custom generate endpoint
    data = custom_generate_audio(payload)

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"Generated audio IDs: {ids}")

    # Polling for the status of the audio generation
    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # Sleep for 5 seconds before polling again
        time.sleep(5)
    return data[0]['audio_url']
#return first gen song URL


