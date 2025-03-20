"""Auto-generated __init__.py for the red_buttons group."""

import click
red_buttons_group = click.Group(name="red_buttons")

__all__ = [
    "supernova",
    "red_buttons_group"
]

from . import supernova


def run_group():
    """Entry point for running the red_buttons command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'red_buttons']
    cli_main()
