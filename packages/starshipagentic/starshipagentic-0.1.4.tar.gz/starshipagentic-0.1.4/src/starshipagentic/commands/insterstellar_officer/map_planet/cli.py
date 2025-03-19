import click
from .services import map_planet_service

@click.command()
@click.argument("input", required=False)
def map_planet_command(input=None):
    """
    Auto-generated CLI command for map_planet.
    """
    result = map_planet_service(input)
    click.echo(result)

if __name__ == "__main__":
    map_planet_command()
