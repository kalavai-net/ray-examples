import requests

response = requests.post("http://127.0.0.1:8000/", json={"text":"Ray Serve is great!"})
print(response)
print(response.text)