# MarkPrompt

MarkPrompt 是一个用于 LLM 的提示词模板引擎。

## 特性

- YAML 元数据支持
- 基于角色的内容块
- 模板变量渲染
- 安全检查机制
- 工具调用功能（Function Calling）

## 安装

```bash
pip install -e .
```

## 使用

```python
from markprompt.client import MarkPromptClient

client = MarkPromptClient("templates")
response = client.generate("example")
```

## 工具调用功能

MarkPrompt支持工具调用功能，允许你将Python函数作为工具传递给LLM，并自动执行被调用的函数。

### 示例

```python
# 定义工具函数
def get_weather(city: str, date: str = "today"):
    """获取指定城市的天气信息"""
    # 实际功能实现
    return f"{city}的{date}天气..."

# 使用工具
response = client.generate(
    "assistant", 
    prompt="北京今天天气怎么样？",
    tools=[get_weather]  # 传递工具函数列表
)
```

更详细的示例请查看 `examples/tools_example.py`