import click
from .services import trycoder_service

@click.command()
@click.argument("input", required=False)
def trycoder_command(input=None):
    """
    Auto-generated CLI command for trycoder.
    """
    result = trycoder_service(input)
    click.echo(result)

if __name__ == "__main__":
    trycoder_command()
