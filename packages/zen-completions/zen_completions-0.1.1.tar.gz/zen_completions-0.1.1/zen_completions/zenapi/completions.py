"""Compatibility module for zenapi integration with zen-completions."""

from typing import List, Dict, Any, Optional
from zen_completions.models.model_router import get_completion, ModelSettings
from zen_completions.models.enums import ModelEnum


def get_choice_from_task(prompt, context, posts, task):
    """
    Compatibility function that matches zenapi's model_router.get_choice_from_task
    
    Args:
        prompt: The prompt object (used to determine model settings)
        context: The system prompt
        posts: List of post objects with text_src and text attributes
        task: The user's message
    
    Returns:
        An object with a content attribute containing the response
    """
    # Convert posts to history format
    history = []
    for post in posts:
        if hasattr(post, 'text_src') and hasattr(post, 'text'):
            if post.text_src in ["USER", "User"]:
                history.append({"role": "user", "content": post.text})
            elif post.text_src in ["ASSISTANT", "Assistant"]:
                history.append({"role": "assistant", "content": post.text})
    
    # Determine model settings based on prompt
    # This is a simplified version - you might need to adjust based on your needs
    model_settings = ModelSettings(
        name=ModelEnum.OPENAI_GPT4O,
        temperature=0.7,
        max_tokens=1000
    )
    
    # If prompt has model settings, try to use them
    try:
        from zenlib.reusable_apps.z_agents.models import ModelSetting
        if hasattr(prompt, 'id'):
            model_setting = ModelSetting.objects.filter(prompt=prompt).order_by("-id").first()
            if model_setting:
                # Map model name to zen-completions enum
                if hasattr(model_setting, 'name'):
                    name_map = {
                        "azure-gpt-4o": ModelEnum.AZURE_OPENAI_GPT4O,
                        "gpt-4o": ModelEnum.OPENAI_GPT4O,
                        "gpt-4-turbo": ModelEnum.OPENAI_GPT4O_TURBO,
                    }
                    model_settings.name = name_map.get(model_setting.name, ModelEnum.OPENAI_GPT4O)
                
                # Set temperature and max_tokens if available
                if hasattr(model_setting, 'temperature'):
                    model_settings.temperature = model_setting.temperature
                if hasattr(model_setting, 'max_tokens'):
                    model_settings.max_tokens = model_setting.max_tokens
    except Exception:
        # Fallback to default settings if anything goes wrong
        pass
    
    # Get completion using zen-completions
    response_content = get_completion(
        prompt=task.strip(),
        context=context,
        history=history,
        model_settings=model_settings
    )
    
    # Return a response object matching zenapi's expected format
    class Response:
        def __init__(self, content):
            self.content = content
    
    return Response(response_content)


# Convenience alias for backward compatibility
# This allows: from zen_completions.zenapi.completions import model_router
model_router = type('ModelRouter', (), {
    'get_choice_from_task': get_choice_from_task
})() 