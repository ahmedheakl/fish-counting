import json 
import requests

# with open("data.json", "r") as f:
#     d = json.load(f)

url = "http://localhost:8000/test"

# response = requests.post(url, json=d)
response = requests.get(url)
print(response.json()["Hello"] == "World")
