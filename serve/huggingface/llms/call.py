import requests
prompt = "Once upon a time, there was a horse"
prompt = """Write a great sales pitch for the company Kalavai, which lets any build and train their own language models, and earn money letting anyone use their gpus

Answer:"""
sample_input = {"text": prompt}
output = requests.post("http://localhost:8000/", json=[sample_input])#.json()
print(output.text)

print(output)
