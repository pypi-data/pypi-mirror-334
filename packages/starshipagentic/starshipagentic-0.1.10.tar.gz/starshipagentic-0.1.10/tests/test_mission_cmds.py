# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Tests for mission commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch
from starshipagentic.commands.mission_cmds import mission_brief, expand_mission, mission_group

@pytest.fixture
def runner():
    """Provide a CLI test runner."""
    return CliRunner()

def test_mission_brief_with_idea(runner):
    """Test mission-brief command with idea provided."""
    result = runner.invoke(mission_group, ["mission-brief", "Create a blog platform"])
    assert result.exit_code == 0
    assert "Generating mission brief for: Create a blog platform" in result.output

def test_mission_brief_with_detailed_flag(runner):
    """Test mission-brief command with detailed flag."""
    result = runner.invoke(mission_group, ["mission-brief", "Create a blog platform", "--detailed"])
    assert result.exit_code == 0
    assert "Creating detailed documentation" in result.output

@patch('starshipagentic.utils.interactive.prompt_for_missing_param')
def test_mission_brief_interactive(mock_prompt, runner):
    """Test mission-brief command with interactive prompt."""
    mock_prompt.return_value = "Interactive blog platform"
    with patch('sys.modules', {'pytest': None}):  # Temporarily remove pytest from sys.modules
        result = runner.invoke(mission_group, ["mission-brief"])
        assert result.exit_code == 0
        assert "Generating mission brief for: Interactive blog platform" in result.output

def test_expand_mission_with_focus(runner):
    """Test expand-mission command with focus provided."""
    result = runner.invoke(mission_group, ["expand-mission", "user-stories"])
    assert result.exit_code == 0
    assert "Expanding mission details for: user-stories" in result.output

@patch('starshipagentic.utils.interactive.prompt_for_missing_param')
def test_expand_mission_interactive(mock_prompt, runner):
    """Test expand-mission command with interactive prompt."""
    mock_prompt.return_value = "database-schema"
    with patch('sys.modules', {'pytest': None}):  # Temporarily remove pytest from sys.modules
        result = runner.invoke(mission_group, ["expand-mission"])
        assert result.exit_code == 0
        assert "Expanding mission details for: database-schema" in result.output
