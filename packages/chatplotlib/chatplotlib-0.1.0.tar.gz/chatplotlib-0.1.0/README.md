[English](README.md) | [中文](./docs/README.zh_cn.md)

# Chatplotlib

Chatplotlib is a Large Language Model auxiliary data visualization tool based on 
matplotlib.

**Attention: The project is in a very early stage of development.**

## Installation

```bash
pip install chatplotlib
```

## Dependencies

- openai>=1.54
- matplotlib>=3.9.0

## Usage

This package is designed for users to conduct data visualization with the assistance of
an LLM (Large Language Model) in an interactive environment, such as a notebook. 
It is generally not a good choice when used in a bare Python script (a `.py` file).  

这个包是为了用户在交互式环境中通过LLM辅助进行数据可视化的，例如notebook；
在裸python脚本（`.py`文件）中，通常不是一个好选择 

```python
from plotter import Plotter
x = [1, 2, 3, 4]
y = [1, 4, 9, 16]
p = Plotter(api_key="sk-xxx") # get from https://aliyun.com/product/tongyi
p.plot("使用下面的变量绘制折线图", x=x, y=y, xlabel="x(s)", ylabel="h(m)")
print(p.get_code())
p.save_session("session.json")
```

## Disclaimer

This project is not affiliated with 
[Matplotlib Developers](https://matplotlib.org/)
or [NumFOCUS](https://numfocus.org/), 
but we do appreciate the work they do.
