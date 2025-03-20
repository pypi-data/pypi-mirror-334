"""Implement a plotter based on LLM."""
import logging

import numpy as np

import chatplotlib as cpl
from chatplotlib.session import Session


_log = logging.getLogger(__name__)


def extract_python_code(text):
    code_blocks = []
    lines = text.splitlines()
    in_code_block = False
    current_block = []
    for line in lines:
        if line.strip().startswith("```python"):
            in_code_block = True
            continue
        if line.strip().startswith("```") and in_code_block:
            in_code_block = False
            code_blocks.append("\n".join(current_block))
            current_block = []
            continue
        if in_code_block:
            current_block.append(line)
    if not code_blocks:
        return None

    # return the longest code block
    longest_code = max(code_blocks, key=len)
    return longest_code


class Plotter:
    """A plotter based on LLM.

    Args:
        id (int, optional): The id of the plotter. Defaults to None.
        api_key (str, optional): The api key of the LLM. Defaults to None. User can get
            personal free api-key from https://www.aliyun.com/product/tongyi.
        base_url (str, optional): LLM Service Url. Defaults to
            "https://dashscope.aliyuncs.com/compatible-mode/v1".
        model_name (str, optional): LLM model name. Defaults to
            "qwen2.5-coder-3b-instruct".

    Examples:
        >>> from plotter import Plotter
        >>> x = [1, 2, 3, 4]
        >>> y = [1, 4, 9, 16]
        >>> p = Plotter(api_key="sk-xxx") # get from https://aliyun.com/product/tongyi
        >>> p.plot("使用下面的变量绘制折线图", x=x, y=y, xlabel="x(s)", ylabel="h(m)")
        >>> print(p.get_code())
        >>> p.save_session("session.json")


    """

    def __init__(
        self,
        id=None,
        api_key=None,
        base_url=None,
        model_name=None,
        temperature=None,
    ):
        self.id = id
        self.session = Session(
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
        )

        self.codes = []

    def plot(self, content, exec_code=True, **kwargs):
        data_info = {}
        for k, v in kwargs.items():
            if isinstance(v, np.ndarray):
                data_info[k] = {
                    "variable name": k,
                    "type": "numpy.ndarray",
                    "shape": v.shape,
                }
            elif isinstance(v, list):
                data_info[k] = {"variable name": k, "type": "list", "length": len(v)}
            else:
                data_info[k] = {"variable name": k, "type": type(v)}

        if data_info:
            content = f"{content}\n请仅使用下方数据，若存在未提供的数据宁可留空也不要自拟：\n{data_info}"

        anwser = self.session.chat(content)
        self.codes.append(extract_python_code(anwser))
        if exec_code:
            self._exec_code(**kwargs)


    def replot(self, content, exec_code=True, **kwargs):
        self.session.pop()
        self.plot(content, exec_code, **kwargs)

    def __repr__(self):
        return f"Plotter(id={self.id}) with {self.session}"

    def _exec_code(self, **kwargs):
        try:
            exec(self.codes[-1], None, kwargs)
            return True
        except Exception as e:
            _log.warning(f"Code execution failed: {e}")
        return False

    def save_session(self, filename):
        self.session.to_json(filename)

    def get_code(self):
        return self.codes[-1]
