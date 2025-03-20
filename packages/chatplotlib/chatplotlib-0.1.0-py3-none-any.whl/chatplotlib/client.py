"""LLM Client

Only test for qwen2.5-coder-3b-instruct now.
"""

from openai import OpenAI
from openai import APIConnectionError, NotFoundError, AuthenticationError


class LLMClient:

    def __init__(self, id=None, api_key=None, base_url=None, model_name=None):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name

        try:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except Exception as e:
            print(type(e), e)

    def chat(self, messages, model_name: str = None, temperature=0.1) -> str:
        if not model_name:
            model_name = self.model_name

        try:
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                # max_tokens=2048,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0,
            )
            return completion
        except APIConnectionError as e:
            print(
                "\033[33mAPIConnectionError:\033[0m",
                e,
                (
                    "\nPlease check your network connection or "
                    f"whether the url {self.base_url} is correct."
                ),
            )
        except NotFoundError as e:
            print("\033[33mNotFoundError:\033[0m", e)
        except AuthenticationError as e:
            print("\033[33mAuthenticationError:\033[0m", e)
        except Exception as e:
            print("\033[33mUnkown Error:\033[0m", e, type(e))
        return False


if __name__ == "__main__":
    client = LLMClient()
    completion = client.chat([{"role": "user", "content": "你好"}])
    if completion:
        print(completion)
