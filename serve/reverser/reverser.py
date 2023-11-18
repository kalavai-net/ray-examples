# File name: model.py
from starlette.requests import Request

import ray
from ray import serve

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 4, "num_gpus": 2})
class Reverser:
    def __init__(self):
        # Load model
        pass

    def reverse(self, text: str) -> str:
        # Run inference
        #model_output = self.model(text)

        # Post-process output to return only the translation text
        #translation = model_output[0]["translation_text"]

        return text["text"][::-1]

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        return self.reverse(english_text)

app = Reverser.bind()
