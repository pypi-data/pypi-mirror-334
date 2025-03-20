"""Chat command for zen-completions."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from zen_completions.models.enums import ModelEnum
from zen_completions.models.model_router import (
    ModelSettings,
    get_completion,
)

console = Console()


@click.command(name="chat")
@click.argument("system_keyword", required=False)
@click.argument("system_content", required=False)
@click.option(
    "--model",
    "-m",
    type=click.Choice([m.value for m in ModelEnum]),
    default=ModelEnum.OPENAI_GPT4O.value,
    help="Model to use for chat.",
)
@click.option(
    "--temperature",
    "-t",
    type=float,
    default=0.7,
    help="Temperature for chat.",
)
@click.option(
    "--max-tokens",
    "-mt",
    type=int,
    default=1000,
    help="Maximum tokens for chat.",
)
@click.option(
    "--system",
    "-s",
    type=str,
    default="You are a helpful assistant.",
    help="System message for chat.",
)
def chat(system_keyword, system_content, model, temperature, max_tokens, system):
    """Interactive chat with LLM.
    
    Examples:
        zen chat
        zen chat system "You are a coding assistant specialized in Python"
    """
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
    
    history = []
    
    if system_message:
        history.append({"role": "system", "content": system_message})
    
    console.print("[bold]Welcome to Zen Chat![/bold]")
    if system_message != system:
        console.print(f"[bold]Using custom system prompt:[/bold] \"{system_message[:50]}{'...' if len(system_message) > 50 else ''}\"")
    console.print("Type 'exit' or 'quit' to end the conversation.")
    console.print()
    
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            history.append({"role": "user", "content": user_input})
            
            with console.status("Thinking..."):
                response = get_completion(
                    prompt=user_input,
                    history=history,
                    model_settings=model_settings,
                )
            
            history.append({"role": "assistant", "content": response})
            
            console.print("[bold green]Assistant[/bold green]")
            console.print(Markdown(response))
            console.print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    console.print("[bold]Goodbye![/bold]")


if __name__ == "__main__":
    chat() 