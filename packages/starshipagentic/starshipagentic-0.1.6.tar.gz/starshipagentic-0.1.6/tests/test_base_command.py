# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Tests for the BaseCommand class."""

import pytest
import click
from unittest.mock import patch, MagicMock
from starshipagentic.utils.base_command import BaseCommand

@pytest.fixture
def base_cmd():
    """Provide a BaseCommand instance."""
    return BaseCommand()

def test_get_param_value_from_arg():
    """Test getting parameter value from argument."""
    base_cmd = BaseCommand()
    result = base_cmd.get_param_value("arg_value", None, "param", "Prompt text")
    assert result == "arg_value"

def test_get_param_value_from_opt():
    """Test getting parameter value from option."""
    base_cmd = BaseCommand()
    result = base_cmd.get_param_value(None, "opt_value", "param", "Prompt text")
    assert result == "opt_value"

def test_get_param_value_opt_overrides_arg():
    """Test that option value overrides argument value."""
    base_cmd = BaseCommand()
    result = base_cmd.get_param_value("arg_value", "opt_value", "param", "Prompt text")
    assert result == "opt_value"

@patch('starshipagentic.utils.interactive.prompt_for_missing_param')
def test_get_param_value_from_prompt(mock_prompt):
    """Test getting parameter value from prompt when both arg and opt are None."""
    mock_prompt.return_value = "prompt_value"
    with patch('sys.modules', {}):  # Remove pytest from sys.modules for this test
        base_cmd = BaseCommand()
        result = base_cmd.get_param_value(None, None, "param", "Prompt text")
        assert result == "prompt_value"
        mock_prompt.assert_called_once_with("param", "Prompt text", choices=None, default=None)

@patch('starshipagentic.utils.interactive.prompt_for_missing_param')
def test_get_param_value_with_choices(mock_prompt):
    """Test getting parameter value with choices."""
    mock_prompt.return_value = "choice1"
    with patch('sys.modules', {}):  # Remove pytest from sys.modules for this test
        base_cmd = BaseCommand()
        choices = ["choice1", "choice2"]
        result = base_cmd.get_param_value(None, None, "param", "Prompt text", choices=choices)
        assert result == "choice1"
        mock_prompt.assert_called_once_with("param", "Prompt text", choices=choices, default=None)

@patch('starshipagentic.utils.interactive.prompt_for_missing_param')
def test_get_param_value_with_default(mock_prompt):
    """Test getting parameter value with default."""
    mock_prompt.return_value = "default_value"
    with patch('sys.modules', {}):  # Remove pytest from sys.modules for this test
        base_cmd = BaseCommand()
        result = base_cmd.get_param_value(None, None, "param", "Prompt text", default="default_value")
        assert result == "default_value"
        mock_prompt.assert_called_once_with("param", "Prompt text", choices=None, default="default_value")

def test_parse_args_for_command():
    """Test parsing arguments for a command."""
    base_cmd = BaseCommand()
    
    # Create a mock Click command
    mock_command = MagicMock()
    mock_param1 = MagicMock(spec=click.Argument)
    mock_param1.name = "arg1"
    mock_param2 = MagicMock(spec=click.Option)
    mock_param2.name = "opt1"
    mock_param2.is_flag = False
    
    # Set up the command's parameters
    mock_command.__click_params__ = [mock_param1, mock_param2]
    
    # Create the wrapper function
    wrapper = base_cmd.parse_args_for_command(mock_command)
    
    # Test the wrapper with pytest module present
    with patch('sys.modules', {'pytest': MagicMock()}):
        wrapper()
        mock_command.assert_called_once_with(arg1=None, opt1=None)
