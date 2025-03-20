"""Model router for zen-completions."""

import os
from typing import Dict, List, Optional, Union

from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field

from zen_completions.models.enums import ModelEnum, ProviderEnum
from zen_completions.models.config import get_api_key


class ModelSettings(BaseModel):
    """Model settings."""
    name: ModelEnum = Field(default=ModelEnum.OPENAI_GPT4O)
    temperature: float = Field(default=0.0)
    max_tokens: int = Field(default=1000)


def get_openai(model_settings: Optional[ModelSettings] = None) -> ChatOpenAI:
    """Get OpenAI model."""
    if model_settings is None:
        model_settings = ModelSettings()

    api_key = get_api_key(ProviderEnum.OPENAI)
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(f"No API key found for {ProviderEnum.OPENAI}")

    model_name = "gpt-4o"
    if model_settings.name == ModelEnum.OPENAI_GPT4O_TURBO:
        model_name = "gpt-4-turbo-2024-04-09"

    return ChatOpenAI(
        openai_api_key=api_key,
        model_name=model_name,
        temperature=model_settings.temperature,
        max_tokens=model_settings.max_tokens,
    )


def get_azure_openai(model_settings: Optional[ModelSettings] = None) -> AzureChatOpenAI:
    """Get Azure OpenAI model."""
    if model_settings is None:
        model_settings = ModelSettings(name=ModelEnum.AZURE_OPENAI_GPT4O)

    api_key = get_api_key(ProviderEnum.AZURE_OPENAI)
    if not api_key:
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(f"No API key found for {ProviderEnum.AZURE_OPENAI}")

    # These could be configurable in the future
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    api_base = os.environ.get(
        "AZURE_OPENAI_API_BASE", 
        "https://bac-gpt-model-southcentralus-1.openai.azure.com/openai/deployments/bac-gpt4o-southcentralus/"
    )
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "bac-gpt4o-southcentralus")
    model_name = os.environ.get("AZURE_OPENAI_MODEL_NAME", "gpt-4o")

    return AzureChatOpenAI(
        api_key=api_key,
        base_url=api_base,
        api_version=api_version,
        model_name=model_name,
        temperature=model_settings.temperature,
        max_tokens=model_settings.max_tokens,
    )


def get_llm(model_settings: Optional[ModelSettings] = None):
    """Get LLM based on model settings."""
    if model_settings is None:
        model_settings = ModelSettings()

    if model_settings.name == ModelEnum.AZURE_OPENAI_GPT4O:
        return get_azure_openai(model_settings)
    elif model_settings.name == ModelEnum.OPENAI_GPT4O:
        return get_openai(model_settings)
    elif model_settings.name == ModelEnum.OPENAI_GPT4O_TURBO:
        return get_openai(model_settings)
    else:
        # Default to OpenAI
        return get_openai(model_settings)


def populate_messages(messages: List[Dict], history: List[Dict]) -> List[Dict]:
    """Populate messages with history."""
    for entry in history:
        if entry.get("role") in ["user", "assistant", "system"]:
            messages.append(entry)
    return messages


def get_completion(
    prompt: str, 
    context: Optional[str] = None, 
    history: Optional[List[Dict]] = None,
    model_settings: Optional[ModelSettings] = None
) -> str:
    """Get completion from LLM."""
    llm = get_llm(model_settings)
    
    messages = []
    
    # Add system message if context is provided
    if context:
        messages.append({"role": "system", "content": context})
    
    # Add history if provided
    if history:
        messages = populate_messages(messages, history)
    
    # Add user prompt
    messages.append({"role": "user", "content": prompt})
    
    # Get response
    response = llm.invoke(messages)
    
    return response.content 