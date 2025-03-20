# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Tests for the CLI functionality."""

import pytest
from click.testing import CliRunner
from starshipagentic.cli import main

def test_main_help():
    """Test that the main help command works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Starship Agentic' in result.output

def test_version():
    """Test that the version command works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output.strip().startswith('main, version')
