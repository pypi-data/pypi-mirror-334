import click
from .services import scan_sector_service

@click.command()
@click.argument("input", required=False)
def scan_sector_command(input=None):
    """
    Auto-generated CLI command for scan_sector.
    """
    result = scan_sector_service(input)
    click.echo(result)

if __name__ == "__main__":
    scan_sector_command()
