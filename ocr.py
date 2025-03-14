import base64
import os
#from mistralai import Mistral
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

#client = Mistral(api_key=api_key)

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

def getTexte(image_path):
    #base64_image = encode_image(image_path)
    #ocr_response = client.ocr.process(
    #    model="mistral-ocr-latest",
    #    document={
    #        "type": "image_url",
    #        "image_url": f"data:image/jpeg;base64,{base64_image}" 
    #    }
    #)
    return "ocr_response"


def get_ocr_text(image_url):
    print(image_url)
    url = "https://api.mistral.ai/v1/ocr"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "mistral-ocr-latest",
        "document": {
            "type": "image_url",
            "image_url": image_url
        }
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

