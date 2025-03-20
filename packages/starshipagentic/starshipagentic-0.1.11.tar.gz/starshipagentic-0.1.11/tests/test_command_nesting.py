#!/usr/bin/env python3
# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""
Test command nesting functionality in Starship Agentic CLI.

This test verifies that:
1. Direct command aliases work (e.g., 'visualize-ship')
2. Command groups work (e.g., 'starshipagentic fleet_commander')
3. Nested commands work (e.g., 'starshipagentic fleet_commander visualize-ship')
"""

import unittest
import subprocess
import sys
import os
import re
from unittest.mock import patch

class TestCommandNesting(unittest.TestCase):
    """Test command nesting functionality in Starship Agentic CLI."""

    def run_command(self, command_list):
        """Run a command and return its output and return code."""
        try:
            result = subprocess.run(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def test_direct_command_alias(self):
        """Test that direct command alias 'visualize-ship' works."""
        # Run the visualize-ship command with --help to avoid actual pygame execution
        stdout, stderr, returncode = self.run_command(["visualize-ship", "--help"])
        
        # Check if the command executed successfully
        self.assertEqual(returncode, 0, f"visualize-ship command failed: {stderr}")
        
        # Verify the output contains expected help text for visualize-ship
        self.assertIn("visualize-ship", stdout, "Help output doesn't mention visualize-ship")
        self.assertIn("--ship", stdout, "Help output doesn't mention the --ship option")

    def test_command_group(self):
        """Test that command group 'starshipagentic fleet_commander' works."""
        # Run the fleet_commander group
        stdout, stderr, returncode = self.run_command(["starshipagentic", "fleet_commander"])
        
        # Check if the command executed successfully
        self.assertEqual(returncode, 0, f"fleet_commander group command failed: {stderr}")
        
        # Verify the output contains expected group help text
        self.assertIn("FLEET_COMMANDER", stdout, "Output doesn't contain group name")
        self.assertIn("visualize-ship", stdout, "Output doesn't list visualize-ship command")
        self.assertIn("tour-ship", stdout, "Output doesn't list tour-ship command")
        self.assertIn("commission-ship", stdout, "Output doesn't list commission-ship command")

    def test_nested_command(self):
        """Test that nested command 'starshipagentic fleet_commander visualize-ship' works."""
        # Run the nested command with --help to avoid actual pygame execution
        stdout, stderr, returncode = self.run_command(
            ["starshipagentic", "fleet_commander", "visualize-ship", "--help"]
        )
        
        # Assert that the nested command shows visualize-ship help output.
        self.assertEqual(returncode, 0, f"Command failed unexpectedly: {stderr}")
        self.assertIn("--ship", stdout, "Expected '--ship' option not found in output")
        self.assertIn("Ship to visualize", stdout, "Expected visualize-ship description not found")

    def test_hyphenated_group_name(self):
        """Test that hyphenated group name 'starshipagentic fleet-commander' fails."""
        # Run the command with hyphenated group name
        stdout, stderr, returncode = self.run_command(["starshipagentic", "fleet-commander"])
        
        # This should fail because group names use underscores, not hyphens
        self.assertNotEqual(returncode, 0, "Hyphenated group name should fail but succeeded")
        self.assertIn("No such command", stderr, "Error message doesn't indicate command not found")

if __name__ == "__main__":
    unittest.main()
