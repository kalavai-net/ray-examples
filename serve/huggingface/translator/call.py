import requests

response = requests.post("http://127.0.0.1:8000/", params={"text": "Hello world!"}).json()
print(response)
