import click
from .services import fabricate_infrastructure_service

@click.command()
@click.argument("input", required=False)
def fabricate_infrastructure_command(input=None):
    """
    Auto-generated CLI command for fabricate_infrastructure.
    """
    result = fabricate_infrastructure_service(input)
    click.echo(result)

if __name__ == "__main__":
    fabricate_infrastructure_command()
