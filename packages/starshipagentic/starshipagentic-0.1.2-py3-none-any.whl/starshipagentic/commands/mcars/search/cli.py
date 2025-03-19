import click
from .services import search_service

@click.command()
@click.argument("input", required=False)
def search_command(input=None):
    """
    Auto-generated CLI command for search.
    """
    result = search_service(input)
    click.echo(result)

if __name__ == "__main__":
    search_command()
