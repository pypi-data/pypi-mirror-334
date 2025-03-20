"""Prompt manager for zen-completions."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# Configuration directory - reuse the same directory as for API keys
from zen_completions.models.config import CONFIG_DIR

PROMPTS_FILE = CONFIG_DIR / "prompts.json"


def _load_prompts() -> Dict[str, str]:
    """Load prompts from file."""
    if not PROMPTS_FILE.exists():
        return {}
    
    with open(PROMPTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_prompts(prompts: Dict[str, str]) -> None:
    """Save prompts to file."""
    # Ensure config directory exists
    CONFIG_DIR.mkdir(exist_ok=True, parents=True)
    
    with open(PROMPTS_FILE, "w") as f:
        json.dump(prompts, f, indent=2)
    
    # Set permissions to be readable only by the user
    os.chmod(PROMPTS_FILE, 0o600)


def save_prompt(name: str, content: str) -> None:
    """Save a prompt with the given name."""
    prompts = _load_prompts()
    prompts[name] = content
    _save_prompts(prompts)


def get_prompt(name: str) -> Optional[str]:
    """Get a prompt by name."""
    prompts = _load_prompts()
    return prompts.get(name)


def list_prompts() -> Dict[str, str]:
    """List all saved prompts."""
    return _load_prompts()


def delete_prompt(name: str) -> bool:
    """Delete a prompt by name."""
    prompts = _load_prompts()
    
    if name not in prompts:
        return False
    
    del prompts[name]
    _save_prompts(prompts)
    
    return True 