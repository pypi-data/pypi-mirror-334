"""Chatplotlib is a Large Language Model auxiliary data visualization tool based on
matplotlib.

**Attention: The project is in a very early stage of development.**


This project is not affiliated with
[Matplotlib Developers](https://matplotlib.org/)
or [NumFOCUS](https://numfocus.org/),
but we do appreciate the work they do.


author: Yao Wu
email: wuyao1997@qq.com
last update: 2025-03-17
"""

__all__ = [
    "rcParams",
    "chatplotlib_fname",
]


import os
from pathlib import Path
import logging


import toml

_log = logging.getLogger(__name__)

__version__ = "0.1.0"

rcParams = {}

def chatplotlib_fname():

    def gen_candidates():
        yield 'chatplotlibrc.toml'
        try:
            chatplotlibrc = os.environ['CHATPLOTLIBRC']
        except KeyError:
            pass
        else:
            yield chatplotlibrc
            yield os.path.join(chatplotlibrc, "chatplotlibrc.toml")
        yield os.path.join(Path.home()/".matplotlib", "chatplotlibrc.toml")

        yield os.path.join(str(Path(__file__).parent), "chatplotlibrc.toml")

    for fname in gen_candidates():
        if os.path.exists(fname) and not os.path.isdir(fname):
            return fname

def _load_rcParams(filename=None):
    global rcParams

    if filename is None:
        filename = chatplotlib_fname()

    with open(filename, "r", encoding="utf-8") as file:
        rcParams = toml.load(filename)
    _log.info(f"Loaded rcParams from {filename}")


_load_rcParams()
