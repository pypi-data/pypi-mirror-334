import click
from .services import plot_navigation_service

@click.command()
@click.argument("input", required=False)
def plot_navigation_command(input=None):
    """
    Auto-generated CLI command for plot_navigation.
    """
    result = plot_navigation_service(input)
    click.echo(result)

if __name__ == "__main__":
    plot_navigation_command()
