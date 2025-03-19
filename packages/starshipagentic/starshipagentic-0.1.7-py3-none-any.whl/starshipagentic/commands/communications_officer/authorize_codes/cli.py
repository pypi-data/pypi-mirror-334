import click
from .services import authorize_codes_service

@click.command()
@click.argument("input", required=False)
def authorize_codes_command(input=None):
    """
    Auto-generated CLI command for authorize_codes.
    """
    result = authorize_codes_service(input)
    click.echo(result)

if __name__ == "__main__":
    authorize_codes_command()
