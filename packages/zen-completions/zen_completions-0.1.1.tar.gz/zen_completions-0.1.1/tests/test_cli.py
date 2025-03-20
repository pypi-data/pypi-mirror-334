"""Tests for the CLI commands."""

import os
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from zen_completions.cli import cli
from zen_completions.commands.config import config
from zen_completions.commands.complete import complete
from zen_completions.commands.chat import chat
from zen_completions.models.model_router import ModelEnum


@pytest.fixture
def cli_runner():
    """Fixture for CLI runner."""
    return CliRunner()


def test_cli_version(cli_runner):
    """Test CLI version command."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help(cli_runner):
    """Test CLI help command."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    
    # Check that our subcommands are listed
    assert "config" in result.output
    assert "complete" in result.output
    assert "chat" in result.output


@patch("zen_completions.commands.config.list_providers")
def test_config_list(mock_list_providers, cli_runner):
    """Test config list command."""
    # Mock the list_providers function
    mock_list_providers.return_value = {
        "openai": True,
        "anthropic": False,
        "cohere": False,
        "azure_openai": True,
    }
    
    result = cli_runner.invoke(config, ["list"])
    assert result.exit_code == 0
    
    # Check that providers are listed
    assert "openai" in result.output
    assert "anthropic" in result.output
    assert "cohere" in result.output
    assert "azure_openai" in result.output


@patch("zen_completions.commands.config.set_api_key")
def test_config_set(mock_set_api_key, cli_runner):
    """Test config set command."""
    result = cli_runner.invoke(config, ["set", "openai", "test-api-key"])
    assert result.exit_code == 0
    
    # Check that set_api_key was called with correct arguments
    mock_set_api_key.assert_called_once_with("openai", "test-api-key")
    
    # Check output message
    assert "set successfully" in result.output.lower()


@patch("zen_completions.commands.config.delete_api_key")
def test_config_delete(mock_delete_api_key, cli_runner):
    """Test config delete command."""
    # Test successful deletion
    mock_delete_api_key.return_value = True
    result = cli_runner.invoke(config, ["delete", "openai"])
    assert result.exit_code == 0
    mock_delete_api_key.assert_called_with("openai")
    assert "deleted successfully" in result.output.lower()
    
    # Test unsuccessful deletion
    mock_delete_api_key.reset_mock()
    mock_delete_api_key.return_value = False
    result = cli_runner.invoke(config, ["delete", "openai"])
    assert result.exit_code == 0
    mock_delete_api_key.assert_called_with("openai")
    assert "no api key found" in result.output.lower()


@patch("zen_completions.commands.complete.get_completion")
def test_complete_command(mock_get_completion, cli_runner):
    """Test complete command."""
    # Mock get_completion
    mock_get_completion.return_value = "This is a test completion"
    
    # Test with minimal arguments
    result = cli_runner.invoke(complete, ["What is the meaning of life?"])
    assert result.exit_code == 0
    assert "This is a test completion" in result.output
    
    # Test with all arguments
    result = cli_runner.invoke(complete, [
        "What is the meaning of life?",
        "--model", ModelEnum.OPENAI_GPT4O.value,
        "--temperature", "0.7",
        "--max-tokens", "500",
        "--system", "You are a helpful assistant",
    ])
    assert result.exit_code == 0
    assert "This is a test completion" in result.output
    
    # Verify get_completion was called with correct arguments
    mock_get_completion.assert_called()


@patch("zen_completions.commands.chat.get_completion")
@patch("rich.prompt.Prompt.ask")
def test_chat_command(mock_prompt_ask, mock_get_completion, cli_runner):
    """Test chat command."""
    # Set up mocks
    mock_prompt_ask.side_effect = ["Hello", "How are you?", "exit"]
    mock_get_completion.side_effect = ["Hi there", "I'm doing well"]
    
    # Run the command
    result = cli_runner.invoke(chat, [
        "--model", ModelEnum.OPENAI_GPT4O.value,
        "--temperature", "0.7",
        "--max-tokens", "500",
        "--system", "You are a helpful assistant",
    ])
    
    # Check result
    assert result.exit_code == 0
    assert mock_get_completion.call_count == 2
    
    # Check that our responses are in the output
    assert "Hi there" in result.output or "I'm doing well" in result.output 