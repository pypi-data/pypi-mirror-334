"""
MarkPrompt core models.
"""
from typing import Dict, Optional

from pydantic import BaseModel, Field


Metadata = dict
GenerationConfig = dict


class PromptTemplate(BaseModel):
    """Main prompt template model."""
    metadata: Metadata
    roles: Optional[Dict[str, str]] = Field(None, description="Role configurations as prefix strings")
    generation_config: GenerationConfig = Field(default_factory=dict)
    input_variables: Dict[str, str] = Field(default_factory=dict, description="Default values for input variables in the template")
    messages: list = Field(default_factory=list, description="Parsed messages from template content")
