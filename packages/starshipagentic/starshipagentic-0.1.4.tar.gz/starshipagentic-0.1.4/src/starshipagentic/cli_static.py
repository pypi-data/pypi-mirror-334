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
Starship Agentic CLI - Static Content
This file contains the static parts of the CLI that don't change during generation.
"""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

def enhance_group_help(group, name):
    """Enhance a command group with better help text and rich formatting."""
    from rich.table import Table
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from starshipagentic.utils.command_registry import CommandRegistry
    
    def display_rich_help(ctx):
        """Display rich formatted help for the command group."""
        console = Console()
        
        # Get group info from registry
        registry = CommandRegistry()
        group_info = registry.get_group_info(name)
        
        # Create a title panel
        replacement = name.replace('_', ' ')
        description = group_info.get('description', f'Commands for {replacement}')
        
        # Create a fancy panel for the title
        panel = Panel(
            f"[bold cyan]{description}[/bold cyan]",
            title=f"[bold yellow]{name.upper()}[/bold yellow]",
            border_style="blue",
            expand=False
        )
        console.print(panel)
        
        # Create a table for commands
        table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
        table.add_column("Command", style="green bold")
        table.add_column("Aliases", style="yellow")
        table.add_column("Description", style="cyan")
        
        # Add rows for each command
        commands = registry.get_all_commands(name)
        console.print(f"[bold blue]DEBUG:[/bold blue] Group name: {name}")
        console.print(f"[bold blue]DEBUG:[/bold blue] Commands found: {commands}")
        
        if not commands:
            console.print("[italic red]No commands found for this group.[/italic red]")
            console.print("[bold yellow]Available groups in registry:[/bold yellow]")
            all_groups = registry.get_all_groups()
            console.print(f"{all_groups}")
        else:
            for cmd_name, cmd_info in commands.items():
                aliases = registry.get_aliases_for_command(name, cmd_name)
                console.print(f"[bold blue]DEBUG:[/bold blue] Aliases for {cmd_name}: {aliases}")
                alias_str = ", ".join(aliases) if aliases else ""
                description = cmd_info.get("description", "")
                table.add_row(cmd_name, alias_str, description)
            
            console.print(table)
        
        console.print("\n[bold green]Usage:[/bold green] [italic]<command> [OPTIONS] [ARGS][/italic]")
        console.print("[bold green]Help:[/bold green] [italic]<command> --help[/italic] for detailed information about a specific command.\n")
    
    # Override the help formatting for the group
    group.format_help = lambda ctx, formatter: None
    
    # Create a custom callback for the help option
    def custom_help_callback(ctx, param, value):
        if value and ctx.invoked_subcommand is None:
            # Only show group help if no subcommand is specified
            display_rich_help(ctx)
            ctx.exit()
        # Otherwise, let the help flag pass through to the subcommand
    
    # Override the help option to use our custom callback
    for param in group.params:
        if param.name == 'help':
            param.callback = custom_help_callback
            break
    
    # Store the original callback
    original_callback = group.callback
    
    # Create a new callback that shows help when no subcommand is invoked
    def new_callback(*args, **kwargs):
        import click
        ctx = click.get_current_context()
        # If no subcommand is invoked, show the rich help
        if ctx.invoked_subcommand is None:
            display_rich_help(ctx)
            return ctx.exit()
        
        # Otherwise, call the original callback if it exists
        if original_callback:
            return original_callback(ctx, *args, **kwargs)
    
    # Replace the group's callback
    group.callback = new_callback
    group.invoke_without_command = True
    
    # Set a basic help text for when --help isn't used
    group.help = f"[{name.upper()}] Commands for {name.replace('_', ' ')}"
    
    return group

@click.group(invoke_without_command=True)
@click.option("--all-commands", is_flag=True, help="Display all available commands")
@click.option("--commands-list", is_flag=True, help="Display commands from commands-list.yml")
@click.pass_context
def main(ctx, all_commands, commands_list):
    """Starship Agentic CLI - Your AI-powered command center."""
    import sys
    
    # Debug the command line arguments
    console.print(f"[bold blue]DEBUG: sys.argv: {sys.argv}[/bold blue]")
    
    if ctx.invoked_subcommand is None:
        console.print(Panel("Welcome to Starship Agentic", title="🚀"))
        if all_commands:
            console.print("All commands would be displayed here")
        elif commands_list:
            console.print("Commands from commands-list.yml would be displayed here")
        else:
            console.print("Use --help for more information")
    else:
        console.print(f"[bold red]DEBUG: Delegating control to subcommand: {ctx.invoked_subcommand}[/bold red]")
        
        # Get the subcommand
        sub_cmd = ctx.command.get_command(ctx, ctx.invoked_subcommand)
        if sub_cmd:
            # Special handling for nested commands
            if hasattr(sub_cmd, 'commands') and len(sys.argv) > 3:
                # The format is: starshipagentic group_name command_name [options]
                # So sys.argv[2] should be the command name
                nested_cmd_name = sys.argv[2]
                console.print(f"[bold blue]DEBUG: Looking for nested command: {nested_cmd_name}[/bold blue]")
                
                # Try to get the nested command from the group
                nested_cmd = sub_cmd.get_command(ctx, nested_cmd_name)
                if nested_cmd:
                    console.print(f"[bold green]DEBUG: Found nested command: {nested_cmd_name}[/bold green]")
                    
                    # If --help is in the arguments, we need to show help for the nested command
                    if '--help' in sys.argv:
                        console.print(f"[bold green]DEBUG: Showing help for nested command: {nested_cmd_name}[/bold green]")
                        help_ctx = click.Context(nested_cmd, parent=ctx, info_name=nested_cmd_name)
                        click.echo(nested_cmd.get_help(help_ctx))
                        return ctx.exit()
                    
                    # Otherwise, invoke the nested command with the remaining args
                    # Remove the first 3 arguments (starshipagentic, group_name, command_name)
                    remaining_args = sys.argv[3:]
                    console.print(f"[bold blue]DEBUG: Remaining args for nested command: {remaining_args}[/bold blue]")
                    
                    # Create a new context for the nested command
                    nested_ctx = click.Context(nested_cmd, parent=ctx, info_name=nested_cmd_name)
                    
                    # Invoke the nested command directly
                    return nested_cmd.main(remaining_args, standalone_mode=False)
            
            # Otherwise, invoke the subcommand normally
            return ctx.invoke(sub_cmd)
        else:
            console.print(f"[bold red]DEBUG: Subcommand {ctx.invoked_subcommand} not found.[/bold red]")
            ctx.exit()

if __name__ == "__main__":
    main()
