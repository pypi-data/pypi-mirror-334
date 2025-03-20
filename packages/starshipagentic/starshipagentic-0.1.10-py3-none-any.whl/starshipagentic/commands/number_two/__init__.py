"""Auto-generated __init__.py for the number_two group."""

import click
number_two_group = click.Group(name="number_two")

__all__ = [
    "expand_mission",
    "mission_brief",
    "number_two_group"
]

from . import expand_mission
from . import mission_brief


def run_group():
    """Entry point for running the number_two command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'number_two']
    cli_main()
