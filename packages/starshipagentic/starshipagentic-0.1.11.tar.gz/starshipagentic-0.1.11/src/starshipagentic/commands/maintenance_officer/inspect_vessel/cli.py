import click
from .services import inspect_vessel_service

@click.command()
@click.argument("input", required=False)
def inspect_vessel_command(input=None):
    """
    Auto-generated CLI command for inspect_vessel.
    """
    result = inspect_vessel_service(input)
    click.echo(result)

if __name__ == "__main__":
    inspect_vessel_command()
