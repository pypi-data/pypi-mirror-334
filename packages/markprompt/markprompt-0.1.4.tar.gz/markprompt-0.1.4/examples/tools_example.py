"""
使用 MarkPrompt 的 tools 功能的示例。
"""

import os

from openai import OpenAI

from src.markprompt import MarkPromptClient
from src.markprompt.core.logger import setup_logger

# 配置日志
logger = setup_logger(__name__)

# OpenAI配置
api_key = os.environ.get("OPENAI_API_KEY", "sk-...")  # 替换为你的API密钥
base_url = "http://127.0.0.1:10240/v1"  # 或你的自定义基础URL

openai = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=30
)


# 定义一些工具函数
def get_weather(city: str, date: str):
    """获取指定城市的天气信息

    Args:
        city (str): 城市名称
        date (str, optional): 日期。默认为"today"

    Returns:
        str: 天气信息
    """
    # 实际应用中，这里会调用天气API
    weather_data = {
        "beijing": {"today": "晴朗，26°C", "tomorrow": "多云，24°C"},
        "shanghai": {"today": "多云，28°C", "tomorrow": "小雨，25°C"},
        "guangzhou": {"today": "晴朗，32°C", "tomorrow": "晴朗，31°C"}
    }

    city = city.lower().strip()
    if city in weather_data and date in weather_data[city]:
        return weather_data[city][date]

    # 尝试处理中文城市名称
    city_map = {"北京": "beijing", "上海": "shanghai", "广州": "guangzhou"}
    if city in city_map and city_map[city] in weather_data and date in weather_data[city_map[city]]:
        return weather_data[city_map[city]][date]

    return f"无法获取{city}的{date}天气信息"


def calculate(expression: str):
    """计算简单的数学表达式"""
    try:
        # 警告：在实际应用中应当添加安全检查
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


def demonstrate_tools():
    """演示工具调用功能"""
    # 创建客户端
    client = MarkPromptClient(
        template_dir=os.path.join(os.path.dirname(__file__), "prompts"),
        client=openai
    )

    try:

        # 准备用户问题
        user_question = "北京今天天气怎么样？另外，请帮我计算 123 + 456 的结果。"

        # 使用工具
        response = client.generate(
            "assistant",  # 使用assistant模板
            user_question,  # 用户问题
            tools=[get_weather, calculate],  # 传递工具函数
            verbose=True  # 启用详细日志
        )
        logger.info(response)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logger.error("处理过程中发生错误", {
            "error": str(e),
            "traceback": error_traceback
        })
        print(f"\n错误详情: {str(e)}")
        print(error_traceback)


if __name__ == "__main__":
    demonstrate_tools()
