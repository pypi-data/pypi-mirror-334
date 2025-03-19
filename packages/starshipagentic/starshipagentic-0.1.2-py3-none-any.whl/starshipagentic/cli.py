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
        sub_cmd = ctx.command.get_command(ctx, ctx.invoked_subcommand)
        if sub_cmd:
            return ctx.invoke(sub_cmd)
        else:
            console.print(f"[bold red]DEBUG: Subcommand {ctx.invoked_subcommand} not found.[/bold red]")
            ctx.exit()

#!/usr/bin/env python3
"""
AUTO-GENERATED FILE – DO NOT EDIT MANUALLY.
This file is generated by the sync2_aliases.py tool.
It contains all dynamic imports, group themes/icons, and group help registration code.
"""

# [AUTO-GENERATED COMMAND IMPORTS START]
from starshipagentic.commands.fleet_commander import run_group as fleet_commander
from starshipagentic.commands.number_two import run_group as number_two
from starshipagentic.commands.engineering_officer import run_group as engineering_officer
from starshipagentic.commands.navigation_officer import run_group as navigation_officer
from starshipagentic.commands.communications_officer import run_group as communications_officer
from starshipagentic.commands.insterstellar_officer import run_group as insterstellar_officer
from starshipagentic.commands.captains_orders import run_group as captains_orders
from starshipagentic.commands.tactical_officer import run_group as tactical_officer
from starshipagentic.commands.maintenance_officer import run_group as maintenance_officer
from starshipagentic.commands.red_buttons import run_group as red_buttons
from starshipagentic.commands.gitmaster import run_group as gitmaster
from starshipagentic.commands.mcars import run_group as mcars
from starshipagentic.commands.droids import run_group as droids
from starshipagentic.commands.fleet_commander.tour_ship.cli import tour_ship_command as tour_ship
from starshipagentic.commands.fleet_commander.tour_ship.cli import tour_ship_command as tour
from starshipagentic.commands.fleet_commander.commission_ship.cli import commission_ship_command as commission_ship
from starshipagentic.commands.fleet_commander.commission_ship.cli import commission_ship_command as commission
from starshipagentic.commands.fleet_commander.visualize_ship.cli import visualize_ship_command as visualize_ship
from starshipagentic.commands.number_two.mission_brief.cli import mission_brief_command as mission_brief
from starshipagentic.commands.number_two.mission_brief.cli import mission_brief_command as mission
from starshipagentic.commands.number_two.expand_mission.cli import expand_mission_command as expand_mission
from starshipagentic.commands.number_two.expand_mission.cli import expand_mission_command as expand
from starshipagentic.commands.engineering_officer.review_schematics.cli import review_schematics_command as review_schematics
from starshipagentic.commands.engineering_officer.review_schematics.cli import review_schematics_command as schematics
from starshipagentic.commands.engineering_officer.calibrate_technology.cli import calibrate_technology_command as calibrate_technology
from starshipagentic.commands.engineering_officer.calibrate_technology.cli import calibrate_technology_command as calibrate
from starshipagentic.commands.navigation_officer.plot_navigation.cli import plot_navigation_command as plot_navigation
from starshipagentic.commands.navigation_officer.plot_navigation.cli import plot_navigation_command as navigation
from starshipagentic.commands.navigation_officer.set_waypoints.cli import set_waypoints_command as set_waypoints
from starshipagentic.commands.navigation_officer.set_waypoints.cli import set_waypoints_command as waypoints
from starshipagentic.commands.communications_officer.authorize_codes.cli import authorize_codes_command as authorize_codes
from starshipagentic.commands.communications_officer.authorize_codes.cli import authorize_codes_command as authorize
from starshipagentic.commands.communications_officer.scan_sector.cli import scan_sector_command as scan_sector
from starshipagentic.commands.communications_officer.scan_sector.cli import scan_sector_command as scan
from starshipagentic.commands.communications_officer.receive_transmission.cli import receive_transmission_command as receive_transmission
from starshipagentic.commands.communications_officer.receive_transmission.cli import receive_transmission_command as transmission
from starshipagentic.commands.insterstellar_officer.map_planet.cli import map_planet_command as map_planet
from starshipagentic.commands.insterstellar_officer.map_planet.cli import map_planet_command as map
from starshipagentic.commands.insterstellar_officer.build_landing_zone.cli import build_landing_zone_command as build_landing_zone
from starshipagentic.commands.insterstellar_officer.build_landing_zone.cli import build_landing_zone_command as buildlz
from starshipagentic.commands.insterstellar_officer.fabricate_infrastructure.cli import fabricate_infrastructure_command as fabricate_infrastructure
from starshipagentic.commands.insterstellar_officer.fabricate_infrastructure.cli import fabricate_infrastructure_command as fabricate
from starshipagentic.commands.captains_orders.warp_speed.cli import warp_speed_command as warp_speed
from starshipagentic.commands.captains_orders.warp_speed.cli import warp_speed_command as warp
from starshipagentic.commands.captains_orders.trycoder.cli import trycoder_command as trycoder
from starshipagentic.commands.captains_orders.engage.cli import engage_command as engage
from starshipagentic.commands.tactical_officer.fire_photons.cli import fire_photons_command as fire_photons
from starshipagentic.commands.tactical_officer.fire_photons.cli import fire_photons_command as photons
from starshipagentic.commands.tactical_officer.aim_lasers.cli import aim_lasers_command as aim_lasers
from starshipagentic.commands.tactical_officer.aim_lasers.cli import aim_lasers_command as lasers
from starshipagentic.commands.tactical_officer.shields_up.cli import shields_up_command as shields_up
from starshipagentic.commands.tactical_officer.shields_up.cli import shields_up_command as shields
from starshipagentic.commands.maintenance_officer.create_checkpoint.cli import create_checkpoint_command as create_checkpoint
from starshipagentic.commands.maintenance_officer.create_checkpoint.cli import create_checkpoint_command as checkpoint
from starshipagentic.commands.maintenance_officer.restore_checkpoint.cli import restore_checkpoint_command as restore_checkpoint
from starshipagentic.commands.maintenance_officer.restore_checkpoint.cli import restore_checkpoint_command as restore
from starshipagentic.commands.maintenance_officer.inspect_vessel.cli import inspect_vessel_command as inspect_vessel
from starshipagentic.commands.maintenance_officer.inspect_vessel.cli import inspect_vessel_command as inspect
from starshipagentic.commands.maintenance_officer.complexity_report.cli import complexity_report_command as complexity_report
from starshipagentic.commands.maintenance_officer.complexity_report.cli import complexity_report_command as complexity
from starshipagentic.commands.red_buttons.supernova.cli import supernova_command as supernova
from starshipagentic.commands.gitmaster.teleport.cli import teleport_command as teleport
from starshipagentic.commands.mcars.search.cli import search_command as search
from starshipagentic.commands.mcars.transport.cli import transport_command as transport
from starshipagentic.commands.droids.droid_splain.cli import droid_splain_command as droid_splain
from starshipagentic.commands.droids.droid_splain.cli import droid_splain_command as droid
from starshipagentic.commands.droids.man_splain.cli import man_splain_command as man_splain
from starshipagentic.commands.droids.man_splain.cli import man_splain_command as splain
# [AUTO-GENERATED COMMAND IMPORTS END]


# [AUTO-GENERATED GROUP THEMES AND ICONS START]
GROUP_THEMES = {
    "fleet_commander": "white",
    "number_two": "white",
    "engineering_officer": "white",
    "navigation_officer": "white",
    "communications_officer": "white",
    "insterstellar_officer": "white",
    "captains_orders": "white",
    "tactical_officer": "white",
    "maintenance_officer": "white",
    "red_buttons": "white",
    "gitmaster": "white",
    "mcars": "white",
    "droids": "white",
}

GROUP_ICONS = {
    "fleet_commander": "⚙️",
    "number_two": "⚙️",
    "engineering_officer": "⚙️",
    "navigation_officer": "⚙️",
    "communications_officer": "⚙️",
    "insterstellar_officer": "⚙️",
    "captains_orders": "⚙️",
    "tactical_officer": "⚙️",
    "maintenance_officer": "⚙️",
    "red_buttons": "⚙️",
    "gitmaster": "⚙️",
    "mcars": "⚙️",
    "droids": "⚙️",
}

# [AUTO-GENERATED GROUP THEMES AND ICONS END]


def register_dynamic_groups():
    """Register all dynamic command groups with the main CLI."""
    from starshipagentic.cli import main, enhance_group_help
    import importlib
    GROUP_NAMES = ['fleet_commander', 'number_two', 'engineering_officer', 'navigation_officer', 'communications_officer', 'insterstellar_officer', 'captains_orders', 'tactical_officer', 'maintenance_officer', 'red_buttons', 'gitmaster', 'mcars', 'droids']
    for group in GROUP_NAMES:
        mod = importlib.import_module(f'starshipagentic.commands.{group}')
        group_obj = getattr(mod, f'{group}_group', None)
        if group_obj is None:
            continue
        enhanced = enhance_group_help(group_obj, group)
        main.add_command(enhanced, group)


from starshipagentic.cli_generated import register_dynamic_groups
register_dynamic_groups()


if __name__ == "__main__":
    main()
