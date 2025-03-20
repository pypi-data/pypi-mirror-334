# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Test script to verify command execution and error handling."""

import sys
import subprocess
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def run_command(command):
    """Run a command and return the result."""
    console.print(f"[bold cyan]Testing: starshipagentic {command}[/bold cyan]")
    
    try:
        result = subprocess.run(
            f"starshipagentic {command}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green]✓ Command succeeded[/green]")
            return True, result.stdout
        else:
            console.print(f"[red]✗ Command failed with code {result.returncode}[/red]")
            console.print(f"Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        console.print(f"[red]✗ Exception: {str(e)}[/red]")
        return False, str(e)

def get_commands_from_registry():
    """Get all commands from the command registry."""
    from starshipagentic.utils.command_registry import command_registry
    
    test_commands = []
    for group_name in command_registry.get_all_groups():
        for cmd_name in command_registry.get_all_commands(group_name):
            # Add parameters for commands that require them to avoid interactive prompts
            if group_name == "vessel" and cmd_name == "commission-ship":
                test_commands.append(f"{group_name} {cmd_name} --template=django-galaxy --name=test-project")
            elif group_name == "mission" and cmd_name == "mission-brief":
                test_commands.append(f"{group_name} {cmd_name} --idea='Test project'")
            else:
                # Basic command without options
                test_commands.append(f"{group_name} {cmd_name}")
    
    return test_commands

def test_basic_commands():
    """Test basic command functionality."""
    console.print(Panel("Testing Basic Commands", style="bold green"))
    
    # Get commands dynamically from registry
    all_commands = get_commands_from_registry()
    
    # Add some commands with options for more thorough testing
    commands_with_options = [
        "vessel commission-ship --template=django-galaxy --name=test-project",
        "vessel visualize-ship --ship=enterprise",
        "architecture review-schematics --type=system"
    ]
    
    # Use a subset of commands for faster testing
    commands = all_commands[:2] + commands_with_options
    
    results = []
    for cmd in commands:
        success, output = run_command(cmd)
        results.append((cmd, success))
    
    return results

def get_aliases_from_registry():
    """Get all aliases from the command registry."""
    from starshipagentic.utils.command_registry import command_registry
    
    test_aliases = []
    for group_name in command_registry.get_all_groups():
        for cmd_name in command_registry.get_all_commands(group_name):
            aliases = command_registry.get_aliases_for_command(group_name, cmd_name)
            for alias in aliases:
                test_aliases.append(alias)
    
    return test_aliases

def test_aliases():
    """Test command aliases."""
    console.print(Panel("Testing Command Aliases", style="bold yellow"))
    
    # Get aliases dynamically from registry
    all_aliases = get_aliases_from_registry()
    
    # Add some aliases with options for more thorough testing
    aliases_with_options = [
        "commission --template=django-galaxy --name=test-project",
        "schematics --type=system"
    ]
    
    # Use a subset of aliases for faster testing
    aliases = all_aliases[:3] if len(all_aliases) >= 3 else all_aliases
    if "tour" in all_aliases and "tour" not in aliases:
        aliases[0] = "tour"  # Ensure we test the tour alias if available
    
    # Add aliases with options
    aliases.extend(aliases_with_options)
    
    results = []
    for cmd in aliases:
        success, output = run_command(cmd)
        results.append((cmd, success))
    
    return results

def test_error_handling():
    """Test error handling for invalid commands."""
    console.print(Panel("Testing Error Handling", style="bold red"))
    
    invalid_commands = [
        "vessel --commission-ship",  # Option instead of command
        "vesssel tour-ship",  # Typo in command group
        "vessel tour-ships",  # Typo in command name
        "vessel commission-ship --templat=django-galaxy"  # Typo in option name
    ]
    
    results = []
    for cmd in invalid_commands:
        success, output = run_command(cmd)
        # For error tests, we expect failure
        results.append((cmd, not success))
    
    return results

def test_config_commands():
    """Test commands from configuration files."""
    console.print(Panel("Testing Configuration Commands", style="bold blue"))
    
    # Test the interactive mode which should load from config
    success, output = run_command("")
    
    return [("interactive mode", success)]

def display_results(all_results):
    """Display test results in a table."""
    table = Table(title="Command Test Results")
    table.add_column("Command", style="cyan")
    table.add_column("Result", style="green")
    
    for cmd, success in all_results:
        result = "[green]✓ Passed[/green]" if success else "[red]✗ Failed[/red]"
        table.add_row(cmd, result)
    
    console.print(table)

@click.command()
@click.option("--section", help="Test section to run (basic, aliases, errors, config, all)")
def main(section):
    """Run command execution tests."""
    all_results = []
    
    if section in (None, "all", "basic"):
        all_results.extend(test_basic_commands())
    
    if section in (None, "all", "aliases"):
        all_results.extend(test_aliases())
    
    if section in (None, "all", "errors"):
        all_results.extend(test_error_handling())
    
    if section in (None, "all", "config"):
        all_results.extend(test_config_commands())
    
    display_results(all_results)
    
    # Count failures
    failures = sum(1 for _, success in all_results if not success)
    if failures > 0:
        console.print(f"[bold red]{failures} tests failed[/bold red]")
        sys.exit(1)
    else:
        console.print("[bold green]All tests passed![/bold green]")

if __name__ == "__main__":
    main()
