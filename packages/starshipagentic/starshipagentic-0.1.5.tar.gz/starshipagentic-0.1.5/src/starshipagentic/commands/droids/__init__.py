"""Auto-generated __init__.py for the droids group."""

import click
droids_group = click.Group(name="droids")

__all__ = [
    "droid_splain",
    "man_splain",
    "droids_group"
]

from . import droid_splain
from . import man_splain


def run_group():
    """Entry point for running the droids command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'droids']
    cli_main()
