"""
使用 MarkPrompt 进行文本翻译的示例。
"""
import json

from markprompt import MarkPromptClient
from markprompt.core.logger import setup_logger
from openai import OpenAI
from rich.pretty import pprint

# 配置日志
logger = setup_logger(__name__)

# 通过公司的 proxy 代理的配置
zepp_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjpbeyJ0b2tlbiI6InJlc2VhcmNoIn1dLCJpYXQiOjE2ODY3MDgyMjYsImV4cCI6MTc0OTgzMDM5OSwiYXVkIjoiIiwiaXNzIjoiIiwic3ViIjoiIn0.8GG_9giAWw4zq-1uMxbfiObSFFy88wT4bEM4c4-no90"
zepp_base_url = "https://service-proxy-private-testing-us.zepp.com/openai"
# zepp_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjpbeyJ0b2tlbiI6InJlc2VhcmNoIn1dLCJpYXQiOjE2ODY3MDgyMjYsImV4cCI6MTc0OTgzMDM5OSwiYXVkIjoiIiwiaXNzIjoiIiwic3ViIjoiIn0.8GG_9giAWw4zq-1uMxbfiObSFFy88wT4bEM4c4-no90"
# zepp_base_url = "http://127.0.0.1:10240/v1"
# zepp_base_url = "http://127.0.0.1:10240/v1"

openai = OpenAI(
    api_key=zepp_api_key,
    base_url=zepp_base_url,
    timeout=30
)


def translate_text():
    # 创建客户端实例
    client = MarkPromptClient(
        template_dir="prompts",  # 相对于当前文件的路径
        client=openai
    )

    # 准备翻译文本
    text = """
 500ml 牛奶，300ml咖啡
""".strip()

    try:
        # 直接读取模板文件并解析
        template_path = client.template_dir / "foods.md"
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        # 解析模板
        template = client.parser.parse(template_content)
        
        # 准备输入变量
        input_values = {
            "user_input": text,
            "target_lang": "中文",
            "tone": "正式"
        }
        
        # 生成消息
        messages = client.parser.render(template, input_values)

        if messages[-1]['role'] != 'user':
            messages.append({"role": "user", "content": text})

        # 打印解析后的消息列表
        print(f"\n解析后的模板:")
        pprint(messages)
        pprint(json.dumps(template.__dict__, indent=2, default=lambda o: o.__dict__))
        # for i, msg in enumerate(messages):
        #     print(f"消息 {i+1}:")
        #     print(f"角色: {msg['role']}")
        #     print(f"内容: {msg['content']}\n")
        #
        # # 跳过 API 调用，只验证模板解析
        # print("\n模板解析成功！")
        # return
            
        # 使用翻译模板生成中文翻译
        # response = client.generate(
        #     "translator",
        #     text,
        #     input_variables={
        #         "target_lang": "中文",
        #         "tone": "正式"
        #     },
        #     verbose=True  # 启用详细日志
        # )
        # print(response.choices[0].message.content)


        logger.info("=================")

        # 流式调用
        # for chunk in client.generate(
        #     "translator",
        #     user_input=text,
        #     input_variables={
        #         "target_lang": "中文",
        #         "tone": "正式"
        #     },
        #     stream=True):
        #
        #     if chunk.choices[0].delta.content:
        #         print(chunk.choices[0].delta.content, end="")
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"错误详情: {str(e)}")
        print(f"错误追踪: {error_trace}")
        logger.error("翻译过程中发生错误", {
            "error": str(e),
            "traceback": error_trace
        })


if __name__ == "__main__":
    translate_text()
