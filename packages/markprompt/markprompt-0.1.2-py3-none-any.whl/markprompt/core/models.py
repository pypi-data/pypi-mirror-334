"""
MarkPrompt core models.
"""
from typing import Dict, Optional

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Template metadata model."""
    name: str = Field(..., description="Template unique identifier")
    version: str = Field(..., description="Semantic version")
    author: Optional[str] = Field(None, description="Template author")
    description: Optional[str] = Field(None, description="Template description")
    created_at: Optional[str] = Field(None, description="Creation date")


class GenerationConfig(BaseModel):
    """Generation configuration model.
    
    This model is a wrapper around the OpenAI API parameters. It accepts any valid
    parameter that can be passed to the OpenAI chat.completions.create function.
    
    Required parameters:
        model: The model to use for generation (e.g., "gpt-3.5-turbo")
        
    Optional parameters:
        - temperature: Controls randomness (0-2)
        - max_tokens: Maximum number of tokens to generate
        - top_p: Nucleus sampling threshold (0-1)
        - frequency_penalty: Frequency penalty (-2 to 2)
        - presence_penalty: Presence penalty (-2 to 2)
        - stop: List of strings to stop generation
        - n: Number of completions to generate
        - stream: Whether to stream responses
        - logit_bias: Token bias dictionary
        - user: User identifier
        - seed: Random seed for deterministic results
        - tools: List of tools the model may call
        - tool_choice: Controls when model calls functions
        - response_format: Format for model responses
        
    For detailed parameter descriptions, see:
    https://platform.openai.com/docs/api-reference/chat/create
    """
    model: str

    class Config:
        extra = "allow"

    def model_dump(self) -> dict:
        """Convert to a dictionary suitable for the OpenAI API."""
        data = super().model_dump()
        return {k: v for k, v in data.items() if v is not None}


class PromptTemplate(BaseModel):
    """Main prompt template model."""
    metadata: Metadata
    roles: Optional[Dict[str, str]] = Field(None, description="Role configurations as prefix strings")
    generation_config: GenerationConfig = Field(default_factory=GenerationConfig)
    input_variables: Dict[str, str] = Field(default_factory=dict, description="Default values for input variables in the template")
    messages: list = Field(default_factory=list, description="Parsed messages from template content")
