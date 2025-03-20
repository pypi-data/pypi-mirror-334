# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Test script to verify command sequence execution."""

import sys
import os
import tempfile
import yaml
from rich.console import Console
from rich.panel import Panel
import click

# Import the run_command_sequence function
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from starshipagentic.cli import run_command_sequence

console = Console()

def create_test_config(config_data):
    """Create a temporary config file with the given data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as temp:
        yaml.dump(config_data, temp)
        return temp.name

def generate_test_sequence():
    """Generate a test sequence using available commands."""
    from starshipagentic.utils.command_registry import command_registry
    
    # Get a representative command from each group
    sequence = []
    for group_name in command_registry.get_all_groups():
        commands = command_registry.get_all_commands(group_name)
        if commands and len(sequence) < 3:  # Limit to 3 commands for testing
            # Get the first command from the list or dictionary
            if isinstance(commands, list) and len(commands) > 0:
                first_cmd = commands[0]
            elif isinstance(commands, dict) and len(commands) > 0:
                first_cmd = list(commands.keys())[0]
            else:
                continue  # Skip if no commands
                
            # Add parameters for commands that require them
            if group_name == "vessel" and first_cmd == "commission-ship":
                sequence.append(f"{group_name} {first_cmd} --template=django-galaxy --name=test-project")
            elif group_name == "mission" and first_cmd == "mission-brief":
                sequence.append(f"{group_name} {first_cmd} --idea='Test project'")
            else:
                sequence.append(f"{group_name} {first_cmd}")
    
    return sequence

def test_string_commands():
    """Test command sequences with string commands."""
    console.print(Panel("Testing String Commands", style="bold green"))
    
    # Generate dynamic test sequence
    dynamic_commands = generate_test_sequence()
    
    # Ensure we have at least these specific commands for visualization testing
    specific_commands = [
        "vessel tour-ship",
        "vessel visualize-ship --ship=enterprise"
    ]
    
    config = {
        'commands': specific_commands + [cmd for cmd in dynamic_commands if cmd not in specific_commands][:1]
    }
    
    config_path = create_test_config(config)
    console.print(f"Created test config at: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        run_command_sequence(data['commands'])
        return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False
    finally:
        os.unlink(config_path)

def test_dict_commands():
    """Test command sequences with dictionary commands."""
    console.print(Panel("Testing Dictionary Commands", style="bold yellow"))
    
    config = {
        'commands': [
            {"vessel": {
                "commission-ship": {
                    "template": "django-galaxy",
                    "name": "test-project"
                }
            }}
        ]
    }
    
    config_path = create_test_config(config)
    console.print(f"Created test config at: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        run_command_sequence(data['commands'])
        return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False
    finally:
        os.unlink(config_path)

def test_mixed_commands():
    """Test command sequences with mixed string and dictionary commands."""
    console.print(Panel("Testing Mixed Commands", style="bold blue"))
    
    # Generate dynamic test sequence
    dynamic_commands = generate_test_sequence()
    
    # Always include these specific commands for consistent testing
    commands = [
        "vessel tour-ship",
        {"vessel": {
            "commission-ship": {
                "template": "django-galaxy",
                "name": "test-project"
            }
        }}
    ]
    
    # Add one more command from the dynamic list if available
    if dynamic_commands and "vessel" not in dynamic_commands[0]:
        commands.append(dynamic_commands[0])
    else:
        commands.append("mission mission-brief")
    
    config = {
        'commands': commands
    }
    
    config_path = create_test_config(config)
    console.print(f"Created test config at: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        run_command_sequence(data['commands'])
        return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False
    finally:
        os.unlink(config_path)

@click.command()
@click.option("--section", help="Test section to run (string, dict, mixed, all)")
def main(section):
    """Run command sequence tests."""
    results = []
    
    if section in (None, "all", "string"):
        console.print("[bold]Testing string commands...[/bold]")
        success = test_string_commands()
        results.append(("String commands", success))
    
    if section in (None, "all", "dict"):
        console.print("[bold]Testing dictionary commands...[/bold]")
        success = test_dict_commands()
        results.append(("Dictionary commands", success))
    
    if section in (None, "all", "mixed"):
        console.print("[bold]Testing mixed commands...[/bold]")
        success = test_mixed_commands()
        results.append(("Mixed commands", success))
    
    # Display results
    console.print("\n[bold]Test Results:[/bold]")
    for test, success in results:
        result = "[green]✓ Passed[/green]" if success else "[red]✗ Failed[/red]"
        console.print(f"{test}: {result}")
    
    # Check if any tests failed
    if any(not success for _, success in results):
        console.print("[bold red]Some tests failed![/bold red]")
        sys.exit(1)
    else:
        console.print("[bold green]All tests passed![/bold green]")

if __name__ == "__main__":
    main()
