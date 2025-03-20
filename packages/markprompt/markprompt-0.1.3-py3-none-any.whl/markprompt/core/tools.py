import inspect
import json
from typing import Any, Callable, Dict, List

from docstring_parser import parse

from .logger import setup_logger

logger = setup_logger(__name__)


class ToolHandler:
    """工具处理器，用于处理工具函数的转换和执行。"""

    def __init__(self, tools: List[Callable] = None, verbose: bool = False):
        """
        初始化工具处理器。
        
        Args:
            tools: 工具函数列表
            verbose: 是否启用详细日志
        """
        self.tools = tools or []
        self.verbose = verbose
        self.tool_map = {tool.__name__: tool for tool in self.tools} if self.tools else {}

    def _parse_docstring(self, docstring: str) -> Dict[str, Any]:
        if not docstring:
            return {"description": "", "params": {}}

        # 使用 docstring_parser 解析文档字符串
        try:
            parsed_docstring = parse(docstring)

            # 获取主要描述
            description = parsed_docstring.short_description or ""

            # 获取参数描述
            params = {}
            for param in parsed_docstring.params:
                params[param.arg_name] = param.description or ""

            return {"description": description, "params": params}
        except Exception as e:
            logger.warning(f"解析文档字符串时出错: {e}")
            return {"description": docstring.strip(), "params": {}}

    def _function_to_openai_tool(self, function: Callable) -> Dict[str, Any]:
        sig = inspect.signature(function)

        # 解析文档字符串
        docstring_info = self._parse_docstring(function.__doc__)

        # 提取主要描述
        func_desc = docstring_info["description"] or f"Function {function.__name__}"

        # 处理参数
        properties = {}
        required_params = []

        for name, param in sig.parameters.items():
            if param.default == inspect.Parameter.empty:
                required_params.append(name)

            param_info = {"type": "string"}

            if param.annotation != inspect.Parameter.empty:
                param_info["type"] = str(param.annotation.__name__)

            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default

            if name in docstring_info["params"]:
                param_info["description"] = docstring_info["params"][name]

            properties[name] = param_info

        return {
            "type": "function",
            "function": {
                "name": function.__name__,
                "description": func_desc,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params
                }
            }
        }

    def convert_tools_to_openai_format(self) -> List[Dict[str, Any]]:
        if not self.tools:
            return []

        return [self._function_to_openai_tool(tool) for tool in self.tools]

    def _format_tool_result(self, tool_call_id: str, function_name: str, result: Any) -> Dict[str, Any]:
        return {
            "tool_call_id": tool_call_id,
            "role": "tool",
            "name": function_name,
            "content": str(result)
        }

    def _handle_tool_execution(self, tool_call: Any) -> Dict[str, Any]:
        function_name = tool_call.function.name
        if function_name not in self.tool_map:
            error_message = f"Error: Tool '{function_name}' not found"
            return self._format_tool_result(
                tool_call.id,
                function_name,
                error_message
            )

        try:
            function_args = json.loads(tool_call.function.arguments)
            result = self.tool_map[function_name](**function_args)
            return self._format_tool_result(tool_call.id, function_name, result)
        except Exception as e:
            error_message = f"Error: {str(e)}"

            if self.verbose:
                logger.error(f"执行工具 {function_name} 时出错: {str(e)}")
            return self._format_tool_result(tool_call.id, function_name, error_message)

    def execute_tool_calls(self, tool_calls: List[Any]) -> List[Dict[str, Any]]:
        if not tool_calls or not self.tools:
            return []

        return [self._handle_tool_execution(tool_call) for tool_call in tool_calls]
