"""Prompt command for zen-completions."""

import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from zen_completions.prompts import (
    get_prompt,
    save_prompt,
    list_prompts,
    delete_prompt,
)

console = Console()


@click.group(name="prompt")
def prompt():
    """Manage system prompts."""
    pass


@prompt.command(name="list")
def list_all_prompts():
    """List all saved prompts."""
    prompts = list_prompts()
    
    if not prompts:
        console.print("[yellow]No prompts found.[/yellow]")
        return
    
    table = Table(title="System Prompts")
    table.add_column("Name", style="cyan")
    table.add_column("Content Preview", style="green")
    
    for name, content in prompts.items():
        # Show preview of the content, truncated if needed
        preview = content[:50] + "..." if len(content) > 50 else content
        table.add_row(name, preview)
    
    console.print(table)


@prompt.command(name="get")
@click.argument("name")
@click.option("--raw", is_flag=True, help="Print the raw prompt without formatting.")
def get_prompt_cmd(name, raw):
    """Get a prompt by name."""
    content = get_prompt(name)
    
    if content is None:
        console.print(f"[red]Prompt not found: {name}[/red]")
        return
    
    if raw:
        console.print(content)
    else:
        console.print(f"[bold cyan]Prompt:[/bold cyan] {name}")
        console.print(Markdown(content))


@prompt.command(name="set")
@click.argument("name")
@click.argument("content", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Load prompt from file.")
def set_prompt_cmd(name, content, file):
    """Set a prompt with the given name."""
    if file:
        with open(file, "r") as f:
            content = f.read()
    elif not content:
        # If no content is provided, open an editor
        content = click.edit(text="", extension=".md")
        
        if content is None:
            console.print("[yellow]No content provided. Prompt not saved.[/yellow]")
            return
    
    save_prompt(name, content)
    console.print(f"[green]Prompt saved: {name}[/green]")


@prompt.command(name="delete")
@click.argument("name")
def delete_prompt_cmd(name):
    """Delete a prompt by name."""
    if delete_prompt(name):
        console.print(f"[green]Prompt deleted: {name}[/green]")
    else:
        console.print(f"[red]Prompt not found: {name}[/red]")


if __name__ == "__main__":
    prompt() 