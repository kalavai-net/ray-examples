import ray
from ray import serve
from fastapi import FastAPI

from transformers import pipeline

app = FastAPI()


@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0, "num_gpus": 1})
@serve.ingress(app)
class Translator:
    def __init__(self):
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    @app.post("/")
    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation


translator_app = Translator.bind()