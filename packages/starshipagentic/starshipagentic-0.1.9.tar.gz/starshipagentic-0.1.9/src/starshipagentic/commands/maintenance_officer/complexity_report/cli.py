import click
from .services import complexity_report_service

@click.command()
@click.argument("input", required=False)
def complexity_report_command(input=None):
    """
    Auto-generated CLI command for complexity_report.
    """
    result = complexity_report_service(input)
    click.echo(result)

if __name__ == "__main__":
    complexity_report_command()
