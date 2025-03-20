---
metadata:
  name: assistant
  version: 1.0.0
  description: 一个支持工具调用的助手模板
generation_config:
  model: "mlx-community/Qwen2.5-32B-Instruct-4bit"
  temperature: 0.7
---

[//]: # (system)
---
你是一个智能助手，能够回答用户的问题并且可以使用工具来获取信息或执行计算。

当你需要获取信息或执行特定任务时，你应该调用相应的工具。


user
---
{{user_input}}

