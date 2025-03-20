"""
日志格式化工具。
"""
import logging
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

# 创建全局控制台实例
console = Console()


def format_tool_calls(tool_calls: List[Any]) -> str:
    """格式化工具调用信息"""
    if not tool_calls:
        return ""

    result = []
    for tool_call in tool_calls:
        if hasattr(tool_call, "function"):
            function_info = tool_call.function
            result.append(f"- {function_info.name}({function_info.arguments})")
        elif isinstance(tool_call, dict) and "function" in tool_call:
            function_info = tool_call["function"]
            name = function_info.get("name", "unknown")
            arguments = function_info.get("arguments", "{}")
            result.append(f"- {name}({arguments})")

    return "\n".join(result)


class DynamicLogger:
    def __init__(self, title: str = "ASSISTANT"):
        self.console = Console()
        self.live = None
        self.title = title
        self.panel_content = Text()

    def __enter__(self):
        self.live = Live(self._render_panel(), console=self.console, refresh_per_second=4)
        self.live.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.live.__exit__(exc_type, exc_val, exc_tb)

    def _render_panel(self):
        return Panel(
            self.panel_content,
            title=self.title,
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )

    def log(self, message: str):
        self.panel_content.append(f"{message}")
        self.live.update(self._render_panel())

    def stop_loading(self):
        pass


class MessageLogger:
    """
    专门用于处理和格式化消息的日志记录器。
    支持各种消息类型的格式化和显示。
    """

    ROLE_STYLES = {
        'system': 'magenta',
        'user': 'blue',
        'assistant': 'green',
        'tools': 'yellow',
        'tool': 'yellow',
        'unknown': 'yellow'
    }

    def __init__(self, logger_name: Optional[str] = None):
        """初始化消息日志记录器"""
        self.logger = setup_logger(logger_name or __name__)
        self.console = Console()

    def _create_panel(self, title: str, content: str, style: str = "blue") -> Panel:
        """创建一个格式化的面板"""
        return Panel(
            content,
            title=title,
            title_align="left",
            border_style=style,
            padding=(1, 2)
        )

    def log_message(self, message: Dict[str, Any]):
        """记录单个消息"""
        try:
            # 获取消息角色和内容
            role = message.get("role", "unknown")
            content = message.get("content", "")

            # 确定面板标题和样式
            title = role.upper()
            style = self.ROLE_STYLES.get(role, "white")

            # 创建并打印面板
            panel = self._create_panel(title, content, style)
            self.console.print(panel)
        except Exception as e:
            self.logger.error(f"Error logging message: {str(e)}")

    def log_messages(self, messages: List[Dict[str, Any]]):
        """记录多个消息"""
        for message in messages:
            self.log_message(message)


def setup_logger(name: str = None) -> logging.Logger:
    """设置日志记录器。"""
    logger = logging.getLogger(name)

    # 如果已经有处理器，不重复添加
    if logger.handlers:
        return logger

    # 使用 RichHandler 替换标准的 StreamHandler
    handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=False,
        show_path=False,
        enable_link_path=False
    )

    # 设置格式为只显示消息内容
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


# 创建全局消息日志记录器实例
message_logger = MessageLogger("message_logger")
