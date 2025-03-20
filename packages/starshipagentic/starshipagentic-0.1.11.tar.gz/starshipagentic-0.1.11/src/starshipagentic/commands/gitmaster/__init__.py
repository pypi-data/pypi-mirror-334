"""Auto-generated __init__.py for the gitmaster group."""

import click
gitmaster_group = click.Group(name="gitmaster")

__all__ = [
    "teleport",
    "gitmaster_group"
]

from . import teleport


def run_group():
    """Entry point for running the gitmaster command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'gitmaster']
    cli_main()
