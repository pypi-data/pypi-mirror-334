"""Auto-generated __init__.py for the navigation_officer group."""

import click
navigation_officer_group = click.Group(name="navigation_officer")

__all__ = [
    "plot_navigation",
    "set_waypoints",
    "navigation_officer_group"
]

from . import plot_navigation
from . import set_waypoints


def run_group():
    """Entry point for running the navigation_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'navigation_officer']
    cli_main()
