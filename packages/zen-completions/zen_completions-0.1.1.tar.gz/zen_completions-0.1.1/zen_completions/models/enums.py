"""Enums for zen-completions."""

from enum import Enum


class ModelEnum(str, Enum):
    """Enum for supported models."""
    AZURE_OPENAI_GPT4O = "azure-gpt-4o"
    OPENAI_GPT4O = "gpt-4o"
    OPENAI_GPT4O_TURBO = "gpt-4-turbo"


class ProviderEnum(str, Enum):
    """Enum for supported providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    AZURE_OPENAI = "azure_openai" 