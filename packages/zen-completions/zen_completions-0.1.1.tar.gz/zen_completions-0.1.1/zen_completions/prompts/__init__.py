"""Prompts module for zen-completions."""

from zen_completions.prompts.manager import (
    get_prompt,
    save_prompt,
    list_prompts,
    delete_prompt,
)

__all__ = ["get_prompt", "save_prompt", "list_prompts", "delete_prompt"] 