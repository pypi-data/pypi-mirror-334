### **Client 设计思想与接口规范**

---

#### **一、核心设计理念**
1. **隐式消息构建**：自动根据模板内容组装符合 OpenAI 规范的 `messages` 数组，开发者只需关注最终用户输入（`prompt`）
2. **角色链继承**：模板中预定义的 `system`/`assistant` 角色内容 + 用户输入的 `prompt` 自动组合为完整对话流
3. **智能变量注入**：`prompt` 自动填充到最后一个 `user` 角色，同时支持模板变量覆盖

---

#### **二、接口定义示例**
```python
class MarkPromptClient:
    def __init__(self, template_dir: str, client: OpenAI = OpenAI()):
        """
        初始化客户端
        :param template_dir: 模板目录路径
        :param client: 可选，默认为 OpenAI 客户端
        """
    
    def generate(
        self,
        template_name: str,
        prompt: str,  # 用户输入内容（自动作为最后一个user角色）
        variables: dict = None,
        **override_params  # 覆盖模板中的generate_config参数
    ) -> str:
        """
        生成对话内容
        :param template_name: 模板文件名（不含.md）
        :param prompt: 用户本次输入内容
        :param variables: 模板变量替换值
        :param override_params: 动态API参数（如model、temperature）
        :return: 模型生成的文本内容
        """
```

---

#### **三、调用示例演示**
**场景**：使用翻译模板，动态指定目标语言

##### **模板文件 (translation.md)**
```markdown
---
metadata:
  name: translation
  version: 1.0.0
roles:
  system:
    prefix: "<|im_start|>system"
    postfix: "<|im_end|>"
generate_config:
  model: gpt-4
  temperature: 0.7
template:
  target_lang: "fr"  # 默认翻译为法语
---
<|im_start|>system
您是专业翻译官，需遵守：
1. 保留术语准确性
2. 使用正式书面语
<|im_end|>
<|im_start|>user
将以下内容翻译为{{ target_lang }}：
{{ user_input }}
<|im_end|>
```

##### **调用代码**
```python
client = MarkPromptClient(template_dir="./prompts", api_key="sk-xxx")

# 示例1：使用默认参数
response = client.generate(
    template_name="translation",
    prompt="Hello World"  # 自动填充到 {{ user_input }}
)

# 示例2：覆盖模板参数
response = client.generate(
    template_name="translation",
    prompt="Good morning",
    variables={"target_lang": "ja"},  # 改为日语
    temperature=0.3  # 覆盖模板的0.7
)
```

##### **实际生成的 OpenAI 请求**
```python
messages = [
    {"role": "system", "content": "您是专业翻译官，需遵守：\n1. 保留术语准确性\n2. 使用正式书面语"},
    {"role": "user", "content": "将以下内容翻译为ja：\nGood morning"}
]

client.chat.completions.create(
    messages=messages,
    model="gpt-4",
    temperature=0.3
)
```

---

#### **四、核心处理规则**

1. **Prompt 注入规则**：
   - 模板中必须包含至少一个 `{{ user_input }}` 占位符（自动替换为 `prompt` 参数）
   - 若存在多个 `user` 角色块，`prompt` 会替换 **最后一个** `{{ user_input }}`

2. **变量优先级**：
   ```python
   final_vars = {
       **template_default_vars,  # 模板中定义的默认值
       **user_provided_vars,     # 用户传入的variables参数
       "user_input": prompt      # 强制注入用户输入
   }
   ```

3. **消息组装逻辑**：
   - 保留模板中 `system`/`assistant` 的历史消息
   - 将渲染后的 `user` 块追加到消息链末尾
   - 自动处理多轮对话上下文

---

#### **五、设计优势**
1. **开发效率**：避免手动拼接复杂的 `messages` 结构
2. **版本可控**：模板修改独立于代码，支持热更新
3. **安全隔离**：用户输入仅影响指定占位符，不会破坏系统指令
4. **灵活扩展**：通过模板快速实现不同风格的对话场景