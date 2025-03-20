import click
from .services import teleport_service

@click.command()
@click.argument("input", required=False)
def teleport_command(input=None):
    """
    Auto-generated CLI command for teleport.
    """
    result = teleport_service(input)
    click.echo(result)

if __name__ == "__main__":
    teleport_command()
