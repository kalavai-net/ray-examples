import pandas as pd

from ray import serve
from starlette.requests import Request


@serve.deployment(ray_actor_options={"num_gpus": 1})
class PredictDeployment:
    def __init__(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
    
        #self.model = AutoModelForCausalLM.from_pretrained(
        #    model_id,
        #    torch_dtype=torch.float32,
        #    #low_cpu_mem_usage=True,
        #    device_map="auto",  # automatically makes use of all GPUs available to the Actor
        #)
        #self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        # These Work!
        #self.model = AutoModelForCausalLM.from_pretrained('roneneldan/TinyStories-33M')
        #self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")

        # Lets test something bigger
        #self.model_id ="microsoft/phi-1_5"
        self.model_id = "HuggingFaceH4/zephyr-7b-beta"

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            device_map="auto"
            )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
    
    def generate(self, text: str) -> pd.DataFrame:
        #input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(
        #    self.model.device
        #)
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        gen_tokens = self.model.generate(
            input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=100,
        )

        return pd.DataFrame(
            self.tokenizer.batch_decode(gen_tokens), columns=["responses"]
        )

    async def __call__(self, http_request: Request) -> str:
        json_request: str = await http_request.json()
        prompts = []
        for prompt in json_request:
            text = prompt["text"]
            if isinstance(text, list):
                prompts.extend(text)
            else:
                prompts.append(text)
        return self.generate(prompts)

deployment = PredictDeployment.bind()