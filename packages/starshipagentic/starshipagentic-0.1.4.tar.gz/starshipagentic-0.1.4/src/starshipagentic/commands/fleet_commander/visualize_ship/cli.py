import click
from starshipagentic.visualization.pygame_display import display_ship_visualization

@click.command()
@click.option('--ship', default='scout', help='Ship to visualize (scout, django, flask, react)')
def visualize_ship_command(ship=None):
    """Launch a Pygame visualization of the specified ship."""
    import sys
    from rich.console import Console
    console = Console()
    
    # Debug information
    console.print(f"[bold blue]DEBUG: visualize_ship_command called with ship={ship}[/bold blue]")
    console.print(f"[bold blue]DEBUG: sys.argv: {sys.argv}[/bold blue]")
    
    if not ship:
        ship = 'scout'  # Default ship
    
    # If --help is in the arguments, we'll just return without launching pygame
    if '--help' in sys.argv:
        return
    
    # Launch the pygame visualization
    display_ship_visualization(ship)
    
    return f"Visualization of {ship} completed."

if __name__ == "__main__":
    visualize_ship_command()
