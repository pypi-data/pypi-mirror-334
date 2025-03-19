import click
from .services import fire_photons_service

@click.command()
@click.argument("input", required=False)
def fire_photons_command(input=None):
    """
    Auto-generated CLI command for fire_photons.
    """
    result = fire_photons_service(input)
    click.echo(result)

if __name__ == "__main__":
    fire_photons_command()
