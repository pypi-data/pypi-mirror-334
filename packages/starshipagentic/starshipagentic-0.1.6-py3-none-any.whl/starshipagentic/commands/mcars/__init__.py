"""Auto-generated __init__.py for the mcars group."""

import click
mcars_group = click.Group(name="mcars")

__all__ = [
    "search",
    "transport",
    "mcars_group"
]

from . import search
from . import transport


def run_group():
    """Entry point for running the mcars command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'mcars']
    cli_main()
