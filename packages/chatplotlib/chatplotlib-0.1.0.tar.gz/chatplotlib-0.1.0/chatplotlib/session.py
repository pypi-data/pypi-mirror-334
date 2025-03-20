"""Session manager for chat with LLM."""

from chatplotlib.client import LLMClient
import json


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


_system_message = """你是一个matplotlib数据可视化专家，下面请辅助我完成数据可视化的任务

## 下面是关于生成代码的具体要求：

1. 使用变量名 fig 和 ax 命名图像和坐标系（子图）对象
2. 如果导入 pyplot 模块，则使用 plt 作为变量名
3. 代码中仅在必要的地方添加少量注释，保持代码简洁
4. 代码块使用"```python\n...\n```"包裹
"""


class Session:

    def __init__(
        self,
        id=None,
        max_tokens=16384,
        temperature=0.1,
        system_message=_system_message,
        api_key=None,
        base_url=None,
        model_name=None,
    ):
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
            print(f"\033[33mWarning: Tokens exceeds limit ({self.max_tokens}).\033[0m")
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
            print("finish_reason:", choice.finish_reason)
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


if __name__ == "__main__":
    session = Session(max_tokens=1024)
    anwser = session.chat("你好")
    print(anwser)

    anwser = session.chat("帮我生成一个python的hello world")
    print(anwser)

    anwser = session.chat("我的上一个请求是什么？")
    print(anwser)

    anwser = session.chat("你还记得上一个问题吗？")
    print(anwser)

    print(session)
