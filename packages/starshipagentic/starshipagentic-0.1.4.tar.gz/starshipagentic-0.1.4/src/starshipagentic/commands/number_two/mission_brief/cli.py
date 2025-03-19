import click
from .services import mission_brief_service

@click.command()
@click.argument("input", required=False)
def mission_brief_command(input=None):
    """
    Auto-generated CLI command for mission_brief.
    """
    result = mission_brief_service(input)
    click.echo(result)

if __name__ == "__main__":
    mission_brief_command()
