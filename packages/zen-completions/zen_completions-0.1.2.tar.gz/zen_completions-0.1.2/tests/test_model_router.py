"""Tests for the model router module."""

import os
import pytest
from unittest.mock import patch, MagicMock

from zen_completions.models.model_router import (
    ModelEnum,
    ModelSettings,
    get_llm,
    get_completion,
    populate_messages,
)


@pytest.fixture
def mock_env_variables():
    """Mock environment variables for testing."""
    original_env = os.environ.copy()
    os.environ["OPENAI_API_KEY"] = "test-api-key"
    os.environ["AZURE_OPENAI_API_KEY"] = "test-azure-key"
    yield
    os.environ.clear()
    os.environ.update(original_env)


class MockLangchainModel:
    """Mock LangChain model for testing."""
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.response_content = "This is a test response"
    
    def invoke(self, messages):
        """Mock invoke method."""
        return MagicMock(content=self.response_content)


def test_populate_messages():
    """Test populate_messages function."""
    # Initial empty messages list
    messages = []
    
    # History with user and assistant messages
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
        {"role": "user", "content": "How are you?"},
        {"role": "system", "content": "Be helpful"},  # Should be included
        {"role": "unknown", "content": "Ignore me"},  # Should be ignored
    ]
    
    # Populate messages
    result = populate_messages(messages, history)
    
    # Check result
    assert len(result) == 4
    assert result[0]["role"] == "user"
    assert result[0]["content"] == "Hello"
    assert result[1]["role"] == "assistant"
    assert result[1]["content"] == "Hi there"
    assert result[2]["role"] == "user"
    assert result[2]["content"] == "How are you?"
    assert result[3]["role"] == "system"
    assert result[3]["content"] == "Be helpful"


@patch("zen_completions.models.model_router.get_api_key", return_value="test-api-key")
@patch("zen_completions.models.model_router.ChatOpenAI", MockLangchainModel)
def test_get_llm_openai(mock_get_api_key):
    """Test get_llm with OpenAI model."""
    # Create model settings for OpenAI
    model_settings = ModelSettings(
        name=ModelEnum.OPENAI_GPT4O,
        temperature=0.7,
        max_tokens=500,
    )
    
    # Get LLM
    llm = get_llm(model_settings)
    
    # Check LLM is correct type
    assert isinstance(llm, MockLangchainModel)
    
    # Check settings are passed correctly
    assert llm.kwargs["temperature"] == 0.7
    assert llm.kwargs["max_tokens"] == 500
    assert llm.kwargs["model_name"] == "gpt-4o"


@patch("zen_completions.models.model_router.get_api_key", return_value="test-azure-key")
@patch("zen_completions.models.model_router.AzureChatOpenAI", MockLangchainModel)
def test_get_llm_azure(mock_get_api_key):
    """Test get_llm with Azure OpenAI model."""
    # Create model settings for Azure OpenAI
    model_settings = ModelSettings(
        name=ModelEnum.AZURE_OPENAI_GPT4O,
        temperature=0.5,
        max_tokens=800,
    )
    
    # Get LLM
    llm = get_llm(model_settings)
    
    # Check LLM is correct type
    assert isinstance(llm, MockLangchainModel)
    
    # Check settings are passed correctly
    assert llm.kwargs["temperature"] == 0.5
    assert llm.kwargs["max_tokens"] == 800


@patch("zen_completions.models.model_router.get_llm")
def test_get_completion(mock_get_llm):
    """Test get_completion function."""
    # Set up mock
    mock_llm = MockLangchainModel()
    mock_llm.response_content = "This is a test completion"
    mock_get_llm.return_value = mock_llm
    
    # Test completion with minimal parameters
    response = get_completion("What is the meaning of life?")
    assert response == "This is a test completion"
    
    # Test completion with all parameters
    context = "You are a helpful assistant"
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    model_settings = ModelSettings(temperature=0.8)
    
    response = get_completion(
        prompt="What is the meaning of life?",
        context=context,
        history=history,
        model_settings=model_settings,
    )
    
    assert response == "This is a test completion"
    
    # Verify correct calls were made
    mock_get_llm.assert_called_with(model_settings) 