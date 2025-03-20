"""Session manager for chat with LLM."""

import logging
import json

import chatplotlib as cpl
from chatplotlib.client import LLMClient


_log = logging.getLogger(__name__)


class TokenUsage:

    def __init__(self):
        self.prompt_tokens = []
        self.completion_tokens = []
        self.total_tokens = []

    def add(self, usage):
        self.prompt_tokens.append(usage.prompt_tokens)
        self.completion_tokens.append(usage.completion_tokens)
        self.total_tokens.append(usage.total_tokens)

    def __repr__(self):
        return (
            f"Tokens(prompt={sum(self.prompt_tokens)}, "
            f"completion={sum(self.completion_tokens)}, "
            f"total={sum(self.total_tokens)}) "
            f"in {len(self.prompt_tokens)} calls."
        )

    def __len__(self):
        return len(self.total_tokens)

    def pop(self):
        self.prompt_tokens.pop()
        self.completion_tokens.pop()
        self.total_tokens.pop()


class Session:

    def __init__(
        self,
        id=None,
        max_tokens=None,
        temperature=None,
        system_message=None,
        api_key=None,
        base_url=None,
        model_name=None,
    ):
        if system_message is None:
            system_message = cpl.rcParams["system_message"]
        if max_tokens is None:
            max_tokens = cpl.rcParams["max_tokens"]
        if temperature is None:
            temperature = cpl.rcParams["temperature"]

        self.id = id
        self.client = LLMClient(
            api_key=api_key, base_url=base_url, model_name=model_name
        )
        self.messages = [{"role": "system", "content": system_message}]
        self.tokens = TokenUsage()
        self.max_tokens = max_tokens
        self._token_out_limit = False
        self.default_temperature = temperature

    def __repr__(self):
        return f"Session(id={self.id}) with {sum(self.tokens.total_tokens)} tokens"

    def chat(self, content):
        if self._token_out_limit:
            _log.warning(f"Warning: Tokens exceeds limit ({self.max_tokens}).")
            return False

        self.messages.append({"role": "user", "content": content})
        completion = self.client.chat(
            self.messages, temperature=self.default_temperature
        )

        if (not completion) or (len(completion.choices) == 0):
            self.messages.pop()
            return False

        choice = completion.choices[0]
        if choice.finish_reason != "stop":
            self.messages.pop()
            _log.warning(f"finish_reason: {choice.finish_reason}")
            return False

        self.tokens.add(completion.usage)
        self.messages.append({"role": "assistant", "content": choice.message.content})

        self._check_token_limit()

        return choice.message.content

    def _check_token_limit(self):
        self._token_out_limit = self.tokens.total_tokens[-1] > self.max_tokens

    def pop(self):
        self.messages.pop()
        self.messages.pop()
        self.tokens.pop()

    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {"id": self.id, "messages": self.messages},
                f,
                ensure_ascii=False,
                indent=2,
            )

