import click
from .services import tour_ship_service

@click.command()
@click.argument("input", required=False)
def tour_ship_command(input=None):
    """
    Auto-generated CLI command for tour_ship.
    """
    result = tour_ship_service(input)
    click.echo(result)

if __name__ == "__main__":
    tour_ship_command()
