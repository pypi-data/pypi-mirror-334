# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Visualization package for Starship Agentic."""

def launch_visualization(ship_name):
    """Launch the visualization interface for the specified ship."""
    try:
        from .pygame_display import display_ship_visualization
        display_ship_visualization(ship_name)
    except ImportError:
        raise ImportError("Pygame is required for visualization features")
