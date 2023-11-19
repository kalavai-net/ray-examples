import requests
prompt = "Once upon a time, there was a horse"
sample_input = {"text": prompt}
output = requests.post("http://localhost:8000/", json=[sample_input])#.json()
print(output.text)

print(output)
