import click
from .services import expand_mission_service

@click.command()
@click.argument("input", required=False)
def expand_mission_command(input=None):
    """
    Auto-generated CLI command for expand_mission.
    """
    result = expand_mission_service(input)
    click.echo(result)

if __name__ == "__main__":
    expand_mission_command()
