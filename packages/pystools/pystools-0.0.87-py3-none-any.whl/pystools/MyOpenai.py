import os

from openai import OpenAI


class client:
    def __init__(self,api_key:str,base_url:str):
        self.api_key = api_key or os.environ["OPENAI_API_KEY"]
        self.base_url = base_url or os.environ["OPENAI_API_BASE"]
        self.openai = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def chat_completions(self, messages: list[dict], model: str = "gpt-3.5-turbo"):

        chat_completion = self.openai.chat.completions.create(
            messages=messages,
            model=model,
        )
        return chat_completion

if __name__ == '__main__':
    api_key = "xxx"
    base_url = "xxx"
    client = client(api_key, base_url)
    print(client.t2t([{"role": "user", "content": "Hello, how are you?"}]))
