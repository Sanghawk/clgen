import click
from click import Group

from clgen.config import Config

openai_command_group = Group("openai", help="OpenAI API settings")


@openai_command_group.command("get-key")
@click.pass_obj
def get_key(cfg: Config):
    """Show your current OpenAI key (masked)."""
    key = cfg.openai_key
    click.echo("No key set." if not key else f"****{key[-4:]}")


@openai_command_group.command("set-key")
@click.argument("key")
@click.pass_obj
def set_key(cfg: Config, key: str):
    """Save a new OpenAI key."""
    cfg.openai_key = key
    click.echo("Key saved.")


@openai_command_group.command("get-model")
@click.pass_obj
def get_model(cfg: Config):
    """Show your current OpenAI model."""
    click.echo(cfg.openai_model)


@openai_command_group.command("set-model")
@click.argument("model")
@click.pass_obj
def set_model(cfg: Config, model: str):
    """Switch your default OpenAI model."""
    cfg.openai_model = model
    click.echo(f"Model set to {model}")
