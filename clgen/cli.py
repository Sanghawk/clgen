# clgen/cli.py
"""
Command-line interface for clgen.
"""
import importlib.metadata
import logging

import click

from .command_groups.config import config_group
from .config import Config

__version__ = importlib.metadata.version("clgen")


@click.group()
@click.version_option(version=__version__, prog_name="clgen")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    ctx.obj = Config()


cli.add_command(config_group)
