import click
from .services import set_waypoints_service

@click.command()
@click.argument("input", required=False)
def set_waypoints_command(input=None):
    """
    Auto-generated CLI command for set_waypoints.
    """
    result = set_waypoints_service(input)
    click.echo(result)

if __name__ == "__main__":
    set_waypoints_command()
