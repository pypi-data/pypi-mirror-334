"""
MarkPrompt template parser.
"""
import logging
import re
from typing import Dict, List, Optional, Tuple

import frontmatter

from .models import PromptTemplate

logger = logging.getLogger(__name__)

DEFAULT_ROLES = {
    "system": "system\n---\n",
    "user": "user\n---\n",
    "assistant": "assistant\n---\n"
}


class TemplateParser:
    """Parser for MarkPrompt templates."""

    def __init__(self):
        self._var_pattern = re.compile(r"{{([a-z_]+)}}")

    def parse(self, content: str) -> PromptTemplate:
        """Parse template content into a PromptTemplate object."""
        metadata, template_content = self._parse_frontmatter(content)

        roles = DEFAULT_ROLES.copy()
        if "roles" in metadata:
            roles.update(metadata["roles"])

        # 解析模板内容为消息列表
        messages = self._parse_messages(template_content, roles)

        template = PromptTemplate(
            metadata=metadata.get("metadata"),
            roles=roles,
            generation_config=metadata.get("generation_config"),
            input_variables=metadata.get("input_variables", {}),
            messages=messages
        )
        return template

    def _parse_messages(self, content: str, roles: Dict[str, str]) -> List[Dict[str, str]]:
        """解析模板内容为消息列表，不替换变量。"""
        # 如果没有角色定义，则将所有内容视为系统消息
        if not roles:
            return [{"role": "system", "content": content.strip()}]

        case_insensitive_roles = {}
        for role, prefix in roles.items():
            role_name = prefix.split('\n')[0]
            case_insensitive_roles[role_name.lower()] = (role, prefix)

        messages = []
        current_pos = 0
        while current_pos < len(content):
            role_match = False
            matched_role = None
            matched_prefix = None

            is_line_start = current_pos == 0 or content[current_pos - 1] == '\n'

            if not is_line_start:
                current_pos += 1
                continue

            for role_name in case_insensitive_roles.keys():
                if current_pos + len(role_name) <= len(content):
                    possible_role = content[current_pos:current_pos + len(role_name)]

                    # 使用大小写不敏感的比较，确保只匹配模板中定义的角色前缀
                    if possible_role.lower() == role_name.lower() and \
                        current_pos + len(role_name) + 5 <= len(content) and \
                        content[current_pos + len(role_name):current_pos + len(role_name) + 5] == '\n---\n':
                        original_role, prefix = case_insensitive_roles[role_name.lower()]
                        role_match = True
                        matched_role = original_role
                        matched_prefix = possible_role + '\n---\n'
                        break

            if not role_match:
                # 没有匹配到任何 role，默认将 content 当作 system message 处理
                messages.append({"role": "system", "content": content.strip()})
                break

            # 查找角色内容结束位置（下一个角色前缀或内容结束）
            start_pos = current_pos + len(matched_prefix)
            end_pos = len(content)

            # 只寻找模板中定义的角色前缀
            for role_name in case_insensitive_roles.keys():
                remaining = content[start_pos:]
                search_pos = 0
                while search_pos < len(remaining):
                    next_pos = remaining.lower().find(role_name.lower(), search_pos)
                    if next_pos == -1:
                        break

                    is_line_start = next_pos == 0 or remaining[next_pos - 1] == '\n'

                    # 检查是否是完整的角色前缀（在行首并包括 \n---\n）
                    possible_role = remaining[next_pos:next_pos + len(role_name)]
                    if is_line_start and next_pos + len(role_name) + 5 <= len(remaining) and \
                        remaining[next_pos + len(role_name):next_pos + len(role_name) + 5] == '\n---\n' and \
                        possible_role.lower() == role_name.lower():
                        # 找到了下一个角色前缀
                        absolute_pos = start_pos + next_pos
                        if absolute_pos < end_pos:
                            end_pos = absolute_pos
                        break

                    search_pos = next_pos + 1

            # 提取消息内容（不替换变量）
            message_content = content[start_pos:end_pos].strip()
            messages.append({
                "role": matched_role,
                "content": message_content
            })

            current_pos = end_pos

        return messages

    def render(self, template: PromptTemplate, input_values: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """根据输入变量渲染模板消息。"""
        # 合并变量，优先使用用户提供的值
        variables = {}
        if template.input_variables:
            variables.update(template.input_variables)
        if input_values:
            variables.update(input_values)

        # 使用已解析的消息列表，替换其中的变量
        rendered_messages = []
        for message in template.messages:
            rendered_content = self._replace_variables(message["content"], variables)
            rendered_messages.append({
                "role": message["role"],
                "content": rendered_content
            })

        return rendered_messages

    def _replace_variables(self, content: str, variables: Dict[str, str]) -> str:
        """Replace variables in content with their values."""
        result = content
        for var_match in self._var_pattern.finditer(content):
            var_name = var_match.group(1)
            var_value = variables.get(var_name)
            if var_value is None:
                logger.warning(f"变量 {var_name} 未找到对应的值")
            else:
                result = result.replace(f"{{{{{var_name}}}}}", var_value)
        return result

    def _parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """Parse frontmatter and content."""
        try:
            post = frontmatter.loads(content)
            if not post.metadata:
                raise ValueError("No metadata found in template")
            return post.metadata, post.content.strip()
        except Exception as e:
            raise ValueError(f"Invalid frontmatter: {e}")
