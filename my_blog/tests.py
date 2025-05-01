import os
from dotenv import load_dotenv
import requests

load_dotenv()
key = os.getenv("HUGGINGFACE_API_TOKEN")
print("KEY:", key)

headers = {"Authorization": f"Bearer {key}"}
payload = {"inputs": "Придумай 5 забавных фокусов"}

response = requests.post("https://api-inference.huggingface.co/models/gpt2", headers=headers, json=payload)
print("RESPONSE:", response.text)