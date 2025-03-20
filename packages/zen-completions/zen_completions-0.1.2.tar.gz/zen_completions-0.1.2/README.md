# Zen Completions

A command-line interface for interacting with various LLM providers through a unified model router.

## Features

- Support for multiple LLM providers (OpenAI, Azure OpenAI)
- Interactive chat mode
- Single completion mode with system prompt support
- Consistent interface across different models

## Installation

### Using pip

```bash
pip install git+https://github.com/zenafide/zen-completions.git
```

### Using poetry

```bash
poetry add git+https://github.com/zenafide/zen-completions.git
```

## Environment Variables

Configure your API keys using environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY=your_openai_api_key

# For Azure OpenAI
export AZURE_OPENAI_API_KEY=your_azure_api_key
export AZURE_OPENAI_API_VERSION=2024-02-15-preview  # Optional
export AZURE_OPENAI_API_BASE=your_base_url  # Optional
export AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment  # Optional
export AZURE_OPENAI_MODEL_NAME=your_model_name  # Optional
```

## Usage

### Interactive Chat

Start an interactive chat session:

```bash
zen chat
```

With a system prompt:

```bash
zen chat system "You are a coding assistant specialized in Python"
```

### Single Completion

Get a single completion:

```bash
zen complete "What is the capital of France?"
```

With a system prompt:

```bash
zen complete "What is the capital of France?" system "You are a geographical expert"
```

### Models and Options

Both commands support these options:

- `--model` or `-m`: Select the model to use
- `--temperature` or `-t`: Set the temperature for generation
- `--max-tokens` or `-mt`: Set the maximum tokens for the response

Example:

```bash
zen complete "Write a Python function to calculate factorial" --model gpt-4o --temperature 0.7 --max-tokens 500
```

## License

MIT 