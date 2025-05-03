# clgen/cli.py
"""
Command-line interface for clgen.
"""
import importlib.metadata
import logging
from pathlib import Path

import click

from .config import Config
from .config_commands import config_command_group
from .utils.cl_generator import ChangelogGenerator
from .utils.git_helpers import get_commits

__version__ = importlib.metadata.version("clgen")

"""
clgen
"""


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


"""
clgen config
"""
cli.add_command(config_command_group)


"""
clgen generate
"""


@cli.command("generate")
@click.option("--since", help="Start point for changelog (tag or commit SHA).")
@click.option(
    "--until", default="HEAD", show_default=True, help="End point for changelog."
)
@click.option("-o", "--output", type=click.Path(dir_okay=False), help="Write to file.")
@click.option(
    "--repo-path",
    type=click.Path(exists=True),
    default=".",
    help="Path to the Git repo.",
)
@click.pass_obj
def generate(
    cfg: Config, since: str, until: str, output: str | None, repo_path: Path | None
):
    """Generate a changelog based on a git repository."""
    if not cfg.openai_key:
        raise click.UsageError(
            "No OpenAI key set. Run `clgen config openai set-key <openai-key>` first."
        )

    repo_path = repo_path if repo_path else Path.cwd()
    commits = get_commits(repo_path, since, until)
    if not commits:
        click.echo("No commits found in that range.", err=True)
        raise SystemExit(1)

    gen = ChangelogGenerator(
        api_key=cfg.openai_key,
        model=cfg.openai_model,
    )
    changelog_md = gen.generate(commits)

    if output:
        Path(output).write_text(changelog_md)
        click.echo(f"Changelog written to {output}")
    else:
        click.echo(changelog_md)
