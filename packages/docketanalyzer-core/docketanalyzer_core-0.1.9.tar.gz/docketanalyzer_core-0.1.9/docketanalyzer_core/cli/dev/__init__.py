import click

from .build import build


@click.group()
def dev():
    """Development CLI commands."""
    pass


dev.add_command(build)
