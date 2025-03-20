"""Test configuration for zen-completions."""

import os
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def disable_api_calls():
    """Disable actual API calls during tests by setting environment variables."""
    # Save original environment
    original_env = os.environ.copy()
    
    # Set dummy API keys to prevent actual API calls
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
    os.environ["AZURE_OPENAI_API_KEY"] = "dummy-azure-key-for-testing"
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env) 