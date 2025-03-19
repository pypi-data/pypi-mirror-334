import click
from .services import receive_transmission_service

@click.command()
@click.argument("input", required=False)
def receive_transmission_command(input=None):
    """
    Auto-generated CLI command for receive_transmission.
    """
    result = receive_transmission_service(input)
    click.echo(result)

if __name__ == "__main__":
    receive_transmission_command()
