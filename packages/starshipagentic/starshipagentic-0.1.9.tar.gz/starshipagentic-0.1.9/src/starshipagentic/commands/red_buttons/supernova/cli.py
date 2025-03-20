import click
from .services import supernova_service

@click.command()
@click.argument("input", required=False)
def supernova_command(input=None):
    """
    Auto-generated CLI command for supernova.
    """
    result = supernova_service(input)
    click.echo(result)

if __name__ == "__main__":
    supernova_command()
