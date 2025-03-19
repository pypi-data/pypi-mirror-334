"""Auto-generated __init__.py for the maintenance_officer group."""

import click
maintenance_officer_group = click.Group(name="maintenance_officer")

__all__ = [
    "complexity_report",
    "create_checkpoint",
    "inspect_vessel",
    "restore_checkpoint",
    "maintenance_officer_group"
]

from . import complexity_report
from . import create_checkpoint
from . import inspect_vessel
from . import restore_checkpoint


def run_group():
    """Entry point for running the maintenance_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'maintenance_officer']
    cli_main()
