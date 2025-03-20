"""Configuration command for zen-completions."""

import click
from rich.console import Console
from rich.table import Table

from zen_completions.models.config import (
    delete_api_key,
    list_providers,
    set_api_key,
)
from zen_completions.models.enums import ProviderEnum

console = Console()


@click.group(name="config")
def config():
    """Configure zen-completions."""
    pass


@config.command(name="list")
def list_config():
    """List configuration."""
    providers = list_providers()
    
    table = Table(title="API Keys")
    table.add_column("Provider", style="cyan")
    table.add_column("Configured", style="green")
    
    for provider, configured in providers.items():
        table.add_row(
            provider,
            "✓" if configured else "✗",
        )
    
    console.print(table)


@config.command(name="set")
@click.argument("provider", type=click.Choice([p.value for p in ProviderEnum]))
@click.argument("api_key")
def set_config(provider, api_key):
    """Set API key for provider."""
    set_api_key(provider, api_key)
    console.print(f"API key for [cyan]{provider}[/cyan] set successfully.")


@config.command(name="delete")
@click.argument("provider", type=click.Choice([p.value for p in ProviderEnum]))
def delete_config(provider):
    """Delete API key for provider."""
    if delete_api_key(provider):
        console.print(f"API key for [cyan]{provider}[/cyan] deleted successfully.")
    else:
        console.print(f"No API key found for [cyan]{provider}[/cyan].")


if __name__ == "__main__":
    config() 