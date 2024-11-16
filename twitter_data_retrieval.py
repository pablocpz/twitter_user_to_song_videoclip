


# # Sample request to get user info
import requests
from io import BytesIO
import base64
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()

bearer_token = os.getenv("SOCIALDATA_API_KEY")



def get_tweets(user_id):
    """returns 29 tweets per api call"""
    url = f"https://api.socialdata.tools/twitter/user/{user_id}/tweets-and-replies"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    tweets = []
    while True:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            tweets.extend(data.get("tweets", []))
            
            # Check if we have collected enough tweets
            if len(tweets) >= 20:
                break
            
            # Check if there is a next_cursor
            next_cursor = data.get("next_cursor")
            if next_cursor:
                url = f"https://api.socialdata.tools/twitter/user/{user_id}/tweets-and-replies?cursor={next_cursor}"
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            break

    # Slice the last 20 tweets if we have more than 20
    # return tweets[-20:] if len(tweets) > 20 else tweets
    return tweets
    
    
    

def get_user_data(user_name):
    """
    get user's bio details , pfp, banner and tweets
    """
    
    
    url = f"https://api.socialdata.tools/twitter/user/{user_name}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Extraer la información del usuario
        user_data = {
            "user_bio": data.get("description"),
            "user_id": data.get("id"),
            "user_creation": data.get("created_at"),
            "user_verified": data.get("verified"),
            "user_followers_count": data.get("followers_count"),
            "user_location": data.get("location"),
            "user_dm": None if data.get("can_dm") == "null" else data.get("can_dm"),
            "user_following_count": data.get("friends_count"),
            "user_privated": data.get("protected")
            # "user_pfp_url": data.get('profile_image_url_https')
        }
        #retrieve around 29 tweets
        tweets = get_tweets(user_id=user_data["user_id"])
        
        user_data["tweets"] = tweets
        
        
        
        
        
        
        
        

        # Descargar la imagen de perfil
        def download_image(url):
            response = requests.get(url)
            if response.status_code == 200:
                # Convertir imagen a base64 para almacenamiento
                image_data = BytesIO(response.content)
                base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
                return base64_image
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
                return None
            
            
        def download_and_resize_image(url):
            """
            for pfp
            """
            response = requests.get(url)
            if response.status_code == 200:
                # Convertir imagen a base64 para almacenamiento
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image = image.resize((224, 224))
                
                # Convertir imagen redimensionada a base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                return base64_image
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
                return None    
            

        # Descargar imagen de perfil
        if data.get('profile_image_url_https'):
            # user_data['user_pfp_base64'] = download_image(data.get('profile_image_url_https'))
            user_pfp_base64 = download_image(data.get('profile_image_url_https'))
        
        # Descargar la imagen de banner
        user_banner_url = data.get('profile_banner_url')
        if user_banner_url:
            user_banner_url += "/1500x500"  # Añadir el tamaño del banner
            banner_image_base64 = download_image(user_banner_url)
            if banner_image_base64:
                # user_data['user_banner_base64'] = banner_image_base64
                user_banner_base64 = banner_image_base64
        else:
            # user_data['user_banner_base64'] = None
            user_banner_base64 = None

        return user_data, list([user_pfp_base64, user_banner_base64])
    #returns the json data , and a list of his pfp and banner in base 64 enc

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# # Ejemplo de uso
# user_info = get_user_data("asciidiego")
# print(user_info)





# import requests
# from io import BytesIO
# import base64
# import requests
# from PIL import Image

# def get_user_data(user_name):
#     url = "https://api.socialdata.tools/twitter/user/asciidiego"
#     headers = {
#         "Authorization": "Bearer 761|vVBCUfOD5KWuvrzYRRQAmuoY4PjHINJZiPhWOn4Ed00936a5",
#         "Accept": "application/json"
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)

#     user_bio = data["description"]
#     user_id = data["id"]
#     user_creation = data["created_at"]   
#     user_verified = data["verified"]
#     user_followers_count = data["followers_count"]
#     user_location = data["location"]
#     #it can be joke or fake locations or different stuff

#     user_dm = None if data["can_dm"] == "null" else data["can_dm"]
#     #maybe we cannot know if the user can be dm'ed or not

#     user_following_count = data["friends_count"]
#     user_privated = data["protected"]

#     user_pfp_url = data['profile_image_url_https']
#     pfp_response = requests.get(user_pfp_url)

#     if pfp_response.status_code == 200:
#         # Guardar la imagen en una variable
#         user_pfp_img = BytesIO(pfp_response.content)
#         print("Imagen almacenada en la variable 'image_data'")
#     else:
#         print(f"Error al descargar la imagen: {pfp_response.status_code}")


#     def download_image(url):
#         response = requests.get(url)
#         if response.status_code == 200:
#             # Convert image to base64 for storage
#             image_data = BytesIO(response.content)
#             base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
            
#             # Return the base64 image data
#             return base64_image
#         else:
#             print(f"Error al descargar la imagen: {response.status_code}")
#             return None

#     # Descargar la imagen de banner
#     user_banner = data.get('profile_banner_url')
#     if user_banner:
#         user_banner += "/1500x500"  # Añadir el tamaño del banner
#         banner_image_base64 = download_image(user_banner)
#         if banner_image_base64:
#             print("Imagen de banner almacenada en base64.")
#     else:
#         print("No se encontró URL de banner para este usuario.")



#     user_banner_img = banner_image_base64


#     print("éxito so far")
