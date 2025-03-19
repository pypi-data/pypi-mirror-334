import click
from .services import build_landing_zone_service

@click.command()
@click.argument("input", required=False)
def build_landing_zone_command(input=None):
    """
    Auto-generated CLI command for build_landing_zone.
    """
    result = build_landing_zone_service(input)
    click.echo(result)

if __name__ == "__main__":
    build_landing_zone_command()
