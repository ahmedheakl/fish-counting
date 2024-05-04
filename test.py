import json 
import requests

with open("data.json", "r") as f:
    d = json.load(f)

url = "http://localhost:8000/fish_feeding"

response = requests.post(url, json=d)
print(response.json())
