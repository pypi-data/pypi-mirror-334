"""Auto-generated __init__.py for the fleet_commander group."""

import click
from .visualize_ship.cli import visualize_ship_command
from .tour_ship.cli import tour_ship_command
from .commission_ship.cli import commission_ship_command

# Create the group and add commands directly
fleet_commander_group = click.Group(name="fleet_commander")
fleet_commander_group.add_command(visualize_ship_command, "visualize-ship")
fleet_commander_group.add_command(tour_ship_command, "tour-ship")
fleet_commander_group.add_command(commission_ship_command, "commission-ship")

# Add a special callback for the group to handle nested commands
original_get_command = fleet_commander_group.get_command

def enhanced_get_command(ctx, cmd_name):
    """Enhanced get_command that handles nested commands better."""
    import sys
    from rich.console import Console
    console = Console()
    
    console.print(f"[bold blue]DEBUG: Enhanced get_command called with {cmd_name}[/bold blue]")
    console.print(f"[bold blue]DEBUG: sys.argv: {sys.argv}[/bold blue]")
    
    # Get the command using the original method
    cmd = original_get_command(ctx, cmd_name)
    
    # Special handling for nested commands
    if cmd_name in ["visualize-ship", "tour-ship", "commission-ship"]:
        console.print(f"[bold green]DEBUG: Special handling for {cmd_name}[/bold green]")
        
        # Return the appropriate command directly
        if cmd_name == "visualize-ship":
            return visualize_ship_command
        elif cmd_name == "tour-ship":
            return tour_ship_command
        elif cmd_name == "commission-ship":
            return commission_ship_command
    
    return cmd

# Replace the get_command method with our enhanced version
fleet_commander_group.get_command = enhanced_get_command

__all__ = [
    "commission_ship",
    "tour_ship",
    "visualize_ship",
    "fleet_commander_group"
]

from . import commission_ship
from . import tour_ship
from . import visualize_ship


def run_group():
    """Entry point for running the fleet_commander command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    original_args = sys.argv.copy()
    
    # When run as a standalone command (e.g., 'fleet_commander visualize-ship')
    # we need to transform it to 'starshipagentic fleet_commander visualize-ship'
    if len(original_args) > 1:
        # The command name is in original_args[0], subcommands start at index 1
        subcommands = original_args[1:]
        
        # Preserve all arguments after the command name
        sys.argv = ['starshipagentic', 'fleet_commander'] + subcommands
    else:
        # No subcommands, just show the group help
        sys.argv = ['starshipagentic', 'fleet_commander']
    
    cli_main()
