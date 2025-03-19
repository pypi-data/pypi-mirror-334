import click
from .services import aim_lasers_service

@click.command()
@click.argument("input", required=False)
def aim_lasers_command(input=None):
    """
    Auto-generated CLI command for aim_lasers.
    """
    result = aim_lasers_service(input)
    click.echo(result)

if __name__ == "__main__":
    aim_lasers_command()
