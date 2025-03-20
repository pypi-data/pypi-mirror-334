import instructor

from openai import OpenAI
from pydantic import BaseModel
from collections.abc import Callable


def create_ollama_client(base_url="http://localhost:11434/v1", api_key="ollama"):
    client  = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    return client


def create_instructor(base_url="http://localhost:11434/v1", api_key="instructor"):
    client = instructor.from_openai(
        OpenAI(
            base_url=base_url,
            api_key=api_key,
        ),
        mode=instructor.Mode.JSON,
    )

    return client

def set_up_task(client, model:str, reply_type:BaseModel, assistant_role="assistant", assistant_prompt:str="You are a helpful assistant.") -> Callable:
    def run(content_input:str) -> type(reply_type):
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": assistant_role,
                    "content": assistant_prompt
                },
                {
                    "role": "user",
                    "content": content_input
                }
            ],
            response_model=reply_type,
        )

        return resp
    return run


