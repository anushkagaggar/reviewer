from llama_cpp import Llama
from pathlib import Path


class LocalLLM:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            temperature=0.2,
            verbose=False
        )

    def generate(self, system_prompt: str, user_input: str) -> str:
        prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_input}

ASSISTANT:
"""
        output = self.llm(prompt, max_tokens=1024)
        return output["choices"][0]["text"]
