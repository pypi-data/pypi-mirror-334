"""Auto-generated __init__.py for the tactical_officer group."""

import click
tactical_officer_group = click.Group(name="tactical_officer")

__all__ = [
    "aim_lasers",
    "fire_photons",
    "shields_up",
    "tactical_officer_group"
]

from . import aim_lasers
from . import fire_photons
from . import shields_up


def run_group():
    """Entry point for running the tactical_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'tactical_officer']
    cli_main()
