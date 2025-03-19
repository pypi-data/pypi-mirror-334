import click
from .services import create_checkpoint_service

@click.command()
@click.argument("input", required=False)
def create_checkpoint_command(input=None):
    """
    Auto-generated CLI command for create_checkpoint.
    """
    result = create_checkpoint_service(input)
    click.echo(result)

if __name__ == "__main__":
    create_checkpoint_command()
