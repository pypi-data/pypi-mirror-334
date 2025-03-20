"""Complete command for zen-completions."""

import click
from rich.console import Console
from rich.markdown import Markdown

from zen_completions.models.enums import ModelEnum
from zen_completions.models.model_router import (
    ModelSettings,
    get_completion,
)

console = Console()


@click.command(name="complete")
@click.argument("prompt")
@click.argument("system_keyword", required=False)
@click.argument("system_content", required=False)
@click.option(
    "--model",
    "-m",
    type=click.Choice([m.value for m in ModelEnum]),
    default=ModelEnum.OPENAI_GPT4O.value,
    help="Model to use for completion.",
)
@click.option(
    "--temperature",
    "-t",
    type=float,
    default=0.0,
    help="Temperature for completion.",
)
@click.option(
    "--max-tokens",
    "-mt",
    type=int,
    default=1000,
    help="Maximum tokens for completion.",
)
@click.option(
    "--system",
    "-s",
    type=str,
    default=None,
    help="System message for completion.",
)
def complete(prompt, system_keyword, system_content, model, temperature, max_tokens, system):
    """Get completion from LLM.
    
    Examples:
        zen complete "What is the capital of France?"
        zen complete "What is the capital of France?" system "You are a geographical expert"
    """
    try:
        model_settings = ModelSettings(
            name=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Determine the system message
        system_message = system
        
        # Check for positional system arguments
        if system_keyword == "system" and system_content:
            system_message = system_content
        
        with console.status("Generating completion..."):
            response = get_completion(
                prompt=prompt,
                context=system_message,
                model_settings=model_settings,
            )
        
        console.print(Markdown(response))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    complete() 