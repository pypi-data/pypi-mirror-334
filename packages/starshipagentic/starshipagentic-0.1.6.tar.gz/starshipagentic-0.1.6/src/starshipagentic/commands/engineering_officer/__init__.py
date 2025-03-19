"""Auto-generated __init__.py for the engineering_officer group."""

import click
engineering_officer_group = click.Group(name="engineering_officer")

__all__ = [
    "calibrate_technology",
    "review_schematics",
    "engineering_officer_group"
]

from . import calibrate_technology
from . import review_schematics


def run_group():
    """Entry point for running the engineering_officer command group directly."""
    import sys
    from starshipagentic.cli import main as cli_main
    sys.argv = ['starshipagentic', 'engineering_officer']
    cli_main()
