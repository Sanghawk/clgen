# clgen/__init__.py
"""
clgen - AI-powered changelog generator
"""

from .cli import cli

__all__ = ["cli"]


def main() -> None:
    """Entry point for the CLI."""
    cli()
