"""Main CLI entry point for zen-completions."""

import click
from rich.console import Console

from zen_completions.commands.chat import chat
from zen_completions.commands.complete import complete
from zen_completions.commands.config import config

console = Console()


@click.group()
@click.version_option()
def cli():
    """Zen Completions - A CLI tool for interacting with LLMs through a model router."""
    pass


# Register commands
cli.add_command(chat)
cli.add_command(complete)
cli.add_command(config)


if __name__ == "__main__":
    cli() 