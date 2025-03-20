"""
MarkPrompt client implementation.
"""
import inspect
import os
from pathlib import Path
from typing import Dict, Optional, Union, List, Callable

from openai import OpenAI

from .core import TemplateParser
from .core.logger import setup_logger, message_logger, DynamicLogger, format_tool_calls
from .core.tools import ToolHandler

logger = setup_logger(__name__)


class MarkPromptClient:
    """Client for generating responses using MarkPrompt templates."""

    def __init__(self, template_dir: Union[str, Path] = '.', client: Optional[OpenAI] = OpenAI()):
        """Initialize the client.
        
        Args:
            template_dir: Directory containing prompt templates. Can be:
            client: Optional OpenAI client instance
        """
        if isinstance(template_dir, str):
            # 处理 ~ 开头的路径
            if template_dir.startswith("~"):
                template_dir = os.path.expanduser(template_dir)

            # 如果是相对路径，从调用者的文件位置开始查找
            if not os.path.isabs(template_dir):
                caller_frame = inspect.stack()[1]
                caller_file = caller_frame.filename
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                template_dir = os.path.join(caller_dir, template_dir)

            template_dir = Path(template_dir)

        if not template_dir.is_dir():
            raise ValueError(f"Template directory not found: {template_dir}")

        self.template_dir = template_dir
        self.client = client
        self.parser = TemplateParser()

    def _generate_with_tools(self, messages, tools: List[Callable], verbose: bool = False, **params):
        # 初始化工具处理器
        tool_handler = ToolHandler(tools=tools, verbose=verbose)
        openai_tools = tool_handler.convert_tools_to_openai_format()
        # Call OpenAI API with streaming support

        with DynamicLogger() as alogger:

            response = self.client.chat.completions.create(
                messages=messages,
                tools=openai_tools,
                **params
            )

            if response.choices[0].message.tool_calls is None:
                panel_content = response.choices[0].message.content
                alogger.log(panel_content)
                return response

            # 记录工具调用
            if verbose:
                content = format_tool_calls(response.choices[0].message.tool_calls)
                alogger.log(content)

            # 执行工具调用
            tool_results = tool_handler.execute_tool_calls(
                response.choices[0].message.tool_calls
            )

            # 如果有工具结果，进行二次请求
            if tool_results:
                try:
                    new_messages = messages.copy()
                    new_messages.append({
                        "role": "assistant",
                        "tool_calls": response.choices[0].message.tool_calls
                    })
                    new_messages.extend(tool_results)
                    second_response = self.client.chat.completions.create(
                        messages=new_messages,
                        **params
                    )

                    if verbose:
                        alogger.log("\n\n")
                        panel_content = second_response.choices[0].message.content
                        alogger.log(panel_content)
                    return second_response
                except Exception as e:
                    if verbose:
                        print(f"{str(e)}")
                        logger.error(f"二次请求失败: {str(e)}")
                        panel_content += f"\n\n生成失败: {str(e)}"
                        logger.error(f"二次请求失败: {panel_content}")
                    return response

    def generate(
        self,
        template_name: str,
        user_input: str,
        input_variables: Optional[Dict[str, str]] = None,
        verbose: bool = False,
        tools: Optional[List[Callable]] = None,
        **override_params
    ):
        """Generate a response using the specified template.
        
        Args:
            template_name: Name of the template file (without .md extension)
            user_input: User input content
            input_variables: Optional template variables
            verbose: Optional flag to enable verbose logging
            tools: Optional list of functions to be converted to OpenAI tools/function calling
            **override_params: Parameters to override template's generate_config,
                             including 'stream' for streamisng output
            
        Returns:
            If override_params contains stream=True, returns a streaming response iterator
            Otherwise, returns the complete response
        """
        # Load and parse template
        template_path = self.template_dir / f"{template_name}.md"
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        with open(template_path, "r", encoding="utf-8") as f:
            template = self.parser.parse(f.read())

        # 准备输入变量
        input_values = input_variables or {}
        input_values["user_input"] = user_input  # 自动注入用户输入

        # Generate messages
        messages = self.parser.render(template, input_values)
        if messages[-1]['role'] != 'user':
            messages.append({"role": "user", "content": user_input})

        if verbose:
            message_logger.log_messages(messages)

        # Prepare generation parameters
        params = {k: v for k, v in template.generation_config.model_dump().items() if v is not None}
        params.update(override_params)

        if tools:
            return self._generate_with_tools(messages, tools, verbose, **params)
        else:
            response = self.client.chat.completions.create(
                messages=messages,
                **params
            )

            if params.get('stream'):
                return response

            if verbose:
                message = response.choices[0].message
                # 使用 message_logger 记录助手消息
                message_logger.log_message(message.__dict__)

            return response
