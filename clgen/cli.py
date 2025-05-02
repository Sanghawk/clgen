# clgen/cli.py
"""
Command-line interface for clgen.
"""
import importlib.metadata
import logging

import click

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


@cli.group()
def config() -> None:
    """Manage settings."""
    pass


@config.group()
def openai() -> None:
    """OpenAI API settings."""
    pass


@openai.command("get-key")
@click.pass_obj
def get_key(cfg: Config) -> None:
    key = cfg.openai_key
    if not key:
        click.echo("No key set.")
    else:
        click.echo(f"****{key[-4:]}")


@openai.command("set-key")
@click.argument("key")
@click.pass_obj
def set_key(cfg: Config, key: str) -> None:
    cfg.openai_key = key
    click.echo("Key saved.")


@openai.command("get-model")
@click.pass_obj
def get_model(cfg: Config) -> None:
    click.echo(cfg.openai_model)


@openai.command("set-model")
@click.argument("model")
@click.pass_obj
def set_model(cfg: Config, model: str) -> None:
    cfg.openai_model = model
    click.echo(f"Model set to {model}")
