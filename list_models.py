
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        models = response.json()['data']
        for model in models:
            print(f"- {model['id']}")
    else:
        print("Error response:", response.text)
except Exception as e:
    print(f"Exception: {e}")
