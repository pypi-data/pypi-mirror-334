import click
from .services import warp_speed_service

@click.command()
@click.argument("input", required=False)
def warp_speed_command(input=None):
    """
    Auto-generated CLI command for warp_speed.
    """
    result = warp_speed_service(input)
    click.echo(result)

if __name__ == "__main__":
    warp_speed_command()
