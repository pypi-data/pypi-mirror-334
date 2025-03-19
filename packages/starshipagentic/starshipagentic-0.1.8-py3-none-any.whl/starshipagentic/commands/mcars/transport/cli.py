import click
from .services import transport_service

@click.command()
@click.argument("input", required=False)
def transport_command(input=None):
    """
    Auto-generated CLI command for transport.
    """
    result = transport_service(input)
    click.echo(result)

if __name__ == "__main__":
    transport_command()
