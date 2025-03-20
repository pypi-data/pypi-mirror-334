import click
from .services import droid_splain_service

@click.command()
@click.argument("input", required=False)
def droid_splain_command(input=None):
    """
    Auto-generated CLI command for droid_splain.
    """
    result = droid_splain_service(input)
    click.echo(result)

if __name__ == "__main__":
    droid_splain_command()
