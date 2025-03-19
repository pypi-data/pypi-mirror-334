import click
from .services import man_splain_service

@click.command()
@click.argument("input", required=False)
def man_splain_command(input=None):
    """
    Auto-generated CLI command for man_splain.
    """
    result = man_splain_service(input)
    click.echo(result)

if __name__ == "__main__":
    man_splain_command()
