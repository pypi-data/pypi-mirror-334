"""Auto-generated __init__.py for the fleet_commander group."""

import click
fleet_commander_group = click.Group(name="fleet_commander")

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
    sys.argv = ['starshipagentic', 'fleet_commander']
    cli_main()
