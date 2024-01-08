import pandas as pd
from typing import Dict, Optional
from ray import serve
from starlette.requests import Request
import os
import json
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_MODEL_ARGS = {
    "low_cpu_mem_usage": True,
    "device_map": "auto",
}

DEFAULT_GENERATE_ARGS = {
    "do_sample": True,
    "temperature": 0.9,
    "max_length": 100,
}

DEFAULT_TOKENIZER_ARGS = {}

DEFAULT_TOKENIZING_ARGS = {}

@serve.deployment(ray_actor_options={"num_gpus": 1})
class PredictDeployment:
    def __init__(self, 
                 model_id: str, 
                 tokenizer_id: Optional[str]=None, 
                 model_args:Optional[Dict]=None, 
                 tokenizer_args:Optional[Dict]=None, 
                 tokenizing_args:Optional[Dict]=None,
                 generate_args:Optional[Dict]=None
            ):

        self.model_args = model_args or DEFAULT_MODEL_ARGS
        self.tokenizing_args = tokenizing_args or DEFAULT_TOKENIZING_ARGS
        self.tokenizer_args = tokenizer_args or DEFAULT_TOKENIZER_ARGS
        self.generate_args = generate_args or DEFAULT_GENERATE_ARGS

        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                **self.model_args
            )
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id or model_id, **self.tokenizer_args)
            logger.info("Model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model or tokenizer: {e}")
            raise e

    def generate(self, text: str, generate_args:Optional[Dict]=None) -> pd.DataFrame:
        generate_args = generate_args or self.generate_args

        try:
            input_ids = self.tokenizer(text, return_tensors="pt", **self.tokenizing_args).input_ids.to(
                self.model.device
            )

            gen_tokens = self.model.generate(
                input_ids,
                **generate_args
            )
            return pd.DataFrame(
                self.tokenizer.batch_decode(gen_tokens), columns=["responses"]
            )
        except Exception as e:
            logger.error(f"Error in generating response: {e}")
            raise e

    async def __call__(self, http_request: Request) -> str:
        try:
            json_request: str = await http_request.json()
            prompts = []
            for prompt in json_request:
                text = prompt["text"]
                if isinstance(text, list):
                    prompts.extend(text)
                else:
                    prompts.append(text)
            return self.generate(prompts)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return str(e)


params = {
    "model_id": os.environ.get("MODEL_ID"),
    "tokenizer_id": os.environ.get("TOKENIZER_ID")
}

json_env_vars = [
    "TOKENIZER_ARGS",
    "TOKENIZING_ARGS",
    "MODEL_ARGS",
    "GENERATE_ARGS",
]

for env_var in json_env_vars:
    env_var_val = os.environ.get(env_var)
    if env_var_val:
        try:
            params[env_var.lower()] = json.loads(env_var_val)
        except:
            logger.info(f"Failed to load env var {env_var} with value {env_var_val}")


deployment = PredictDeployment.bind(**params)
