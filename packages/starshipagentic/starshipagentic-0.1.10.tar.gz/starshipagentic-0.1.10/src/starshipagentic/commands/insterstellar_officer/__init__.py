"""Auto-generated __init__.py for the insterstellar_officer group."""

import click
insterstellar_officer_group = click.Group(name="insterstellar_officer")

__all__ = [
    "build_landing_zone",
    "fabricate_infrastructure",
    "map_planet",
    "insterstellar_officer_group"
]

from . import build_landing_zone
from . import fabricate_infrastructure
from . import map_planet


def run_group():
    """Entry point for running the insterstellar_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'insterstellar_officer']
    cli_main()
