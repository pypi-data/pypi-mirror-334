# Chatplotlib

Chatplotlib 是一个基于 matplotlib 的大型语言模型辅助数据可视化工具。

**注意：该项目目前处于开发阶段。**

## 安装

```bash
pip install chatplotlib
```

## 依赖

- openai>=1.54
- matplotlib>=3.9.0

## 使用方法

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

## 免责声明

按照要求，此项目不隶属于 [Matplotlib Developers](https://matplotlib.org/)
或 [NumFOCUS](https://numfocus.org/)，尽管我们非常欣赏和感激他们的工作。
