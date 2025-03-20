"""Auto-generated __init__.py for the communications_officer group."""

import click
communications_officer_group = click.Group(name="communications_officer")

__all__ = [
    "authorize_codes",
    "receive_transmission",
    "scan_sector",
    "communications_officer_group"
]

from . import authorize_codes
from . import receive_transmission
from . import scan_sector


def run_group():
    """Entry point for running the communications_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'communications_officer']
    cli_main()
