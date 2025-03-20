"""Auto-generated __init__.py for the captains_orders group."""

import click
captains_orders_group = click.Group(name="captains_orders")

__all__ = [
    "engage",
    "trycoder",
    "warp_speed",
    "captains_orders_group"
]

from . import engage
from . import trycoder
from . import warp_speed


def run_group():
    """Entry point for running the captains_orders command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'captains_orders']
    cli_main()
