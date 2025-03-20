import click
from .services import commission_ship_service

@click.command()
@click.argument("input", required=False)
def commission_ship_command(input=None):
    """
    Auto-generated CLI command for commission_ship.
    """
    result = commission_ship_service(input)
    click.echo(result)

if __name__ == "__main__":
    commission_ship_command()
