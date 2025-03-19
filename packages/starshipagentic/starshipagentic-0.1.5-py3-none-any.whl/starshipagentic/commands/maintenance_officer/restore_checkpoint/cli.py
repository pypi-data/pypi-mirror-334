import click
from .services import restore_checkpoint_service

@click.command()
@click.argument("input", required=False)
def restore_checkpoint_command(input=None):
    """
    Auto-generated CLI command for restore_checkpoint.
    """
    result = restore_checkpoint_service(input)
    click.echo(result)

if __name__ == "__main__":
    restore_checkpoint_command()
