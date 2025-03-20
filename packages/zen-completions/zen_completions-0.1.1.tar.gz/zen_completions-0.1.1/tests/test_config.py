"""Tests for the configuration module."""

import os
import tempfile
import pytest
from pathlib import Path

from zen_completions.models.model_router import ProviderEnum
from zen_completions.models.config import (
    set_api_key,
    get_api_key,
    delete_api_key,
    list_providers,
    CONFIG_DIR,
    CONFIG_FILE,
    KEY_FILE,
)


@pytest.fixture
def temp_config():
    """Create temporary config directory for testing."""
    # Save original paths
    original_config_dir = CONFIG_DIR
    original_config_file = CONFIG_FILE
    original_key_file = KEY_FILE
    
    # Create temp dir and update module variables
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Patch the module variables using tempdir
        import zen_completions.models.config as config_module
        config_module.CONFIG_DIR = temp_path
        config_module.CONFIG_FILE = temp_path / "config.json"
        config_module.KEY_FILE = temp_path / "key.bin"
        
        # Ensure directory exists
        temp_path.mkdir(exist_ok=True)
        
        yield
        
        # Restore original paths
        config_module.CONFIG_DIR = original_config_dir
        config_module.CONFIG_FILE = original_config_file
        config_module.KEY_FILE = original_key_file


def test_set_get_api_key(temp_config):
    """Test setting and getting API keys."""
    provider = ProviderEnum.OPENAI
    api_key = "test-api-key-1234"
    
    # Set API key
    set_api_key(provider, api_key)
    
    # Get API key
    retrieved_key = get_api_key(provider)
    
    assert retrieved_key == api_key


def test_delete_api_key(temp_config):
    """Test deleting API keys."""
    provider = ProviderEnum.AZURE_OPENAI
    api_key = "test-azure-key-5678"
    
    # Set API key
    set_api_key(provider, api_key)
    
    # Verify key exists
    assert get_api_key(provider) == api_key
    
    # Delete key
    result = delete_api_key(provider)
    assert result is True
    
    # Verify key is gone
    assert get_api_key(provider) is None
    
    # Try deleting non-existent key
    result = delete_api_key("nonexistent-provider")
    assert result is False


def test_list_providers(temp_config):
    """Test listing providers with configured API keys."""
    # Initially all providers should be unconfigured
    providers = list_providers()
    for provider in ProviderEnum:
        assert providers[provider.value] is False
    
    # Configure a provider
    set_api_key(ProviderEnum.OPENAI, "test-key")
    
    # Check that provider is now configured
    providers = list_providers()
    assert providers[ProviderEnum.OPENAI.value] is True
    
    # Other providers should still be unconfigured
    for provider in ProviderEnum:
        if provider != ProviderEnum.OPENAI:
            assert providers[provider.value] is False 