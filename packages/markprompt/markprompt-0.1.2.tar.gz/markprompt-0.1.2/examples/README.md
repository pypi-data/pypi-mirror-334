# MarkPrompt 示例

这个目录包含了一些使用 MarkPrompt 的实际示例，展示了如何使用 MarkPrompt 来完成各种常见任务。

## 示例列表

### 1. 文本翻译器 (`translator_example.py`)
展示如何使用 MarkPrompt 进行文本翻译。特点：
- 支持多种语言之间的翻译
- 可以控制翻译的语气（正式/非正式）
- 保持原文格式
- 专业术语的特殊处理

### 2. 代码审查助手 (`code_review_example.py`)
展示如何使用 MarkPrompt 进行代码审查。特点：
- 支持多种编程语言
- 可以指定重点关注的方面（性能/安全/可读性等）
- 提供详细的问题分析和改进建议
- 包含代码示例

### 3. 文档生成器 (`doc_generator_example.py`)
展示如何使用 MarkPrompt 自动生成代码文档。特点：
- 支持多种文档风格（Google/NumPy/reStructuredText等）
- 生成完整的接口文档
- 包含使用示例
- 适合自动文档工具处理

### 4. 测试生成器 (`test_generator_example.py`)
展示如何使用 MarkPrompt 生成单元测试。特点：
- 支持多种测试框架（pytest/unittest等）
- 生成全面的测试用例
- 包含边界条件测试
- 遵循测试最佳实践

## 目录结构
```
examples/
├── README.md                # 本文件
├── translator_example.py    # 翻译器示例
├── code_review_example.py  # 代码审查示例
├── doc_generator_example.py # 文档生成器示例
├── test_generator_example.py # 测试生成器示例
└── prompts/                # 提示模板目录
    ├── translator.md       # 翻译器模板
    ├── code_reviewer.md    # 代码审查模板
    ├── doc_generator.md    # 文档生成器模板
    └── test_generator.md   # 测试生成器模板
```

## 使用方法

1. 确保已安装 MarkPrompt：
```bash
pip install markprompt
```

2. 设置 OpenAI API 密钥：
```bash
export OPENAI_API_KEY=your-api-key
```

3. 运行示例：
```bash
# 运行翻译器示例
python translator_example.py

# 运行代码审查示例
python code_review_example.py

# 运行文档生成器示例
python doc_generator_example.py

# 运行测试生成器示例
python test_generator_example.py
```

## 自定义提示模板

每个示例都使用了位于 `prompts/` 目录下的模板文件。你可以根据需要修改这些模板：

1. 调整生成参数（temperature、max_tokens 等）
2. 修改系统提示内容
3. 添加或修改输入变量
4. 更改模型（如从 gpt-3.5-turbo 升级到 gpt-4）

## 注意事项

1. 这些示例仅供参考，实际使用时请根据你的具体需求进行调整
2. 使用 GPT-4 模型可能会产生更好的结果，但成本也会更高
3. 建议在生产环境中添加适当的错误处理和重试机制
