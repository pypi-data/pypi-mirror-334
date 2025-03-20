"""LLM Client

Only test for qwen2.5-coder-3b-instruct now.
"""

import logging

from openai import OpenAI
from openai import APIConnectionError, NotFoundError, AuthenticationError

import chatplotlib as cpl

_log = logging.getLogger(__name__)


class LLMClient:

    def __init__(self, id=None, api_key=None, base_url=None, model_name=None):
        if api_key is None:
            api_key = cpl.rcParams["api_key"]
        if base_url is None:
            base_url = cpl.rcParams["base_url"]
        if model_name is None:
            model_name = cpl.rcParams["model_name"]

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
            _log.warning(
                (
                    f"APIConnectionError:{e}\nPlease check your network "
                    f"connection or whether the url {self.base_url} is correct."
                )
            )
        except NotFoundError as e:
            _log.warning(f"NotFoundError:{e}")
        except AuthenticationError as e:
            _log.warning(f"AuthenticationError:{e}")
        except Exception as e:
            _log.warning(f"Unkown Error:{e}")
        return False


