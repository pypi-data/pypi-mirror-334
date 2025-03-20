# Guide: Replacing zenapi's model_router.py with zen-completions

## Overview

This guide outlines the steps to replace the `model_router.py` file in the zenapi project with functionality from the zen-completions package. The zen-completions package provides a more modular and maintainable implementation with the same functionality.

## Prerequisites

1. Install the zen-completions package:
   ```bash
   pip install zen-completions
   ```

2. Identify all files in the zenapi project that import from or use the `model_router.py` file.

## Step 1: Understanding the Replacement

The zenapi `model_router.py` currently provides these key functions:
- `populate_messages`: Formats conversation posts for LLM consumption
- `get_llm`: Gets the appropriate LLM based on model settings
- `get_choice_from_task`: Gets a response from the LLM for a specific task

The zen-completions package provides compatible replacements through:
- `zen_completions.zenapi.completions.get_choice_from_task`: Direct replacement for zenapi's version
- A mock `model_router` object in `zen_completions.zenapi.completions` for backward compatibility

## Step 2: Updating Imports

For each file that imports from the original `model_router.py`, you'll need to update the imports:

### If importing specific functions:

```python
# Old import
from zenapi.nh_mo_bo.copilot_utils.model_router import get_choice_from_task, populate_messages, get_llm

# New imports
from zen_completions.zenapi.completions import get_choice_from_task
from zen_completions.models.model_router import populate_messages, get_llm
```

### If importing the whole module:

```python
# Old import
from zenapi.nh_mo_bo.copilot_utils import model_router

# New import
from zen_completions.zenapi import completions as model_router
```

### Specific Example: Updating PracticeViewSet and PromptViewSet

In the zenapi `PracticeViewSet` and `PromptViewSet` classes (found in viewsets like `lift/views.py`), the model_router is imported and used in the `run` method:

```python
# Current implementation in PracticeViewSet.run and PromptViewSet.run
from zenapi.nh_mo_bo.copilot_utils import model_router

# Later in the code:
response = model_router.get_choice_from_task(
    prompt, system_prompt, posts, user_message
)
```

This should be updated to:

```python
# Updated implementation
from zen_completions.zenapi import completions as model_router

# The rest of the code remains the same:
response = model_router.get_choice_from_task(
    prompt, system_prompt, posts, user_message
)
```

## Step 3: Handling Model Settings

If your code interacts with model settings, be aware of the differences:

1. zenapi uses database models for settings
2. zen-completions uses a Pydantic model called `ModelSettings`

The compatibility layer in `zen_completions.zenapi.completions` handles this conversion automatically for most cases, but if you have direct interaction with model settings, you might need to update your code:

```python
# Old code
from zenlib.reusable_apps.z_agents.models import ModelSetting
model_setting = ModelSetting.objects.filter(prompt=prompt).first()
llm = get_llm(model_setting)

# New code
from zen_completions.models.model_router import get_llm, ModelSettings
from zen_completions.models.enums import ModelEnum

# Create ModelSettings object
model_settings = ModelSettings(
    name=ModelEnum.OPENAI_GPT4O,  # Or map from your existing setting
    temperature=model_setting.temperature if model_setting else 0.7,
    max_tokens=model_setting.max_tokens if model_setting else 1000
)
llm = get_llm(model_settings)
```

### Handling ModelSettings in zenapi PracticeViewSet

The `zen_completions.zenapi.completions` module handles the conversion between zenapi's database models and zen-completions' Pydantic models. The `get_choice_from_task` function automatically extracts model settings from the `prompt` object, matching the behavior in the original implementation.

## Step 4: Modified API Key Management

The zen-completions package has been modified to look for API keys in the following order:

1. First, it tries to fetch keys from zenapi's database using `AccessKey` model (same as the original zenapi code)
2. If no key is found in the database, it looks in its own config file (`~/.zen-completions/config.json`)
3. Finally, it falls back to environment variables (`OPENAI_API_KEY`, `AZURE_OPENAI_API_KEY`)

This ensures compatibility with existing zenapi installations while maintaining the ability to use zen-completions independently.

Here's how the API key retrieval works now:

```python
# Within zen-completions
def get_api_key(provider):
    """Get API key for provider."""
    # First try zenapi's database
    try:
        from zenlib.reusable_apps.settings.models import AccessKey, ProviderEnum as ZenAPIProviderEnum
        
        # Map provider name
        provider_mapping = {
            "openai": ZenAPIProviderEnum.OPENAI,
            "azure_openai": ZenAPIProviderEnum.AZURE_OPENAI
        }
        
        zenapi_provider = provider_mapping.get(provider)
        if zenapi_provider:
            access_key = AccessKey.objects.filter(name=zenapi_provider).order_by("-id").first()
            if access_key:
                return access_key.get_key()
    except (ImportError, Exception):
        # Fall back to zen-completions' own methods if zenapi is not available
        # or if there was an error accessing the database
        pass
    
    # Then try zen-completions' config file
    # Then fall back to environment variables
    # ... (existing implementation)
```

This means that:

1. No database configuration changes are needed - zen-completions will use the same API keys as zenapi
2. Environment variables in the project's .env file will be used if the database lookup fails
3. zen-completions' own configuration will be used as a last resort

## Step 5: Verification

After making these changes, verify the integration to ensure:

1. All imports are correctly updated
2. The application can connect to the language models
3. The responses are returned in the expected format

## Troubleshooting

### API Key Issues

If you encounter API key errors:
- Check that the database contains valid API keys in the AccessKey model
- Check that the environment variables have the correct names (`OPENAI_API_KEY` and `AZURE_OPENAI_API_KEY`)
- Verify the keys are valid and have necessary permissions

### Import Errors

If you see import errors:
- Ensure zen-completions is installed in the correct environment
- Check for typos in import statements
- Verify the package version is compatible

### Response Format Differences

If you notice differences in response format:
- Check the documentation for any format changes between versions
- The compatibility layer in zen-completions tries to maintain the same format, but edge cases might exist

### Model Settings Not Applied

If model settings are not being applied correctly:
- Verify that the prompt object has the expected model_settings relationship
- Check if the model_setting fields (temperature, max_tokens) are present
- Add logging to the zen_completions.zenapi.completions module to debug the model settings conversion 