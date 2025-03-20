"""Configuration module for zen-completions."""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Union

from cryptography.fernet import Fernet

from zen_completions.models.enums import ProviderEnum

# Configuration directory
CONFIG_DIR = Path.home() / ".zen-completions"
CONFIG_FILE = CONFIG_DIR / "config.json"
KEY_FILE = CONFIG_DIR / "key.bin"

# Ensure config directory exists
CONFIG_DIR.mkdir(exist_ok=True, parents=True)


def _get_encryption_key() -> bytes:
    """Get or create encryption key."""
    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        # Set permissions to be readable only by the user
        os.chmod(KEY_FILE, 0o600)
        return key
    
    with open(KEY_FILE, "rb") as f:
        return f.read()


def _get_cipher_suite() -> Fernet:
    """Get cipher suite for encryption/decryption."""
    key = _get_encryption_key()
    return Fernet(key)


def _load_config() -> Dict:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_config(config: Dict) -> None:
    """Save configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    # Set permissions to be readable only by the user
    os.chmod(CONFIG_FILE, 0o600)


def set_api_key(provider: Union[ProviderEnum, str], api_key: str) -> None:
    """Set API key for provider."""
    if isinstance(provider, ProviderEnum):
        provider = provider.value
    
    config = _load_config()
    
    # Encrypt the API key
    cipher_suite = _get_cipher_suite()
    encrypted_key = cipher_suite.encrypt(api_key.encode()).decode()
    
    # Update config
    if "api_keys" not in config:
        config["api_keys"] = {}
    
    config["api_keys"][provider] = encrypted_key
    
    # Save config
    _save_config(config)


def get_api_key(provider: Union[ProviderEnum, str]) -> Optional[str]:
    """Get API key for provider."""
    if isinstance(provider, ProviderEnum):
        provider = provider.value
    
    config = _load_config()
    
    if "api_keys" not in config or provider not in config["api_keys"]:
        return None
    
    # Decrypt the API key
    cipher_suite = _get_cipher_suite()
    encrypted_key = config["api_keys"][provider]
    
    try:
        return cipher_suite.decrypt(encrypted_key.encode()).decode()
    except Exception:
        return None


def list_providers() -> Dict[str, bool]:
    """List all providers and whether they have API keys configured."""
    config = _load_config()
    result = {}
    
    for provider in ProviderEnum:
        result[provider.value] = False
    
    if "api_keys" in config:
        for provider, _ in config["api_keys"].items():
            if provider in result:
                result[provider] = True
    
    return result


def delete_api_key(provider: Union[ProviderEnum, str]) -> bool:
    """Delete API key for provider."""
    if isinstance(provider, ProviderEnum):
        provider = provider.value
    
    config = _load_config()
    
    if "api_keys" not in config or provider not in config["api_keys"]:
        return False
    
    del config["api_keys"][provider]
    _save_config(config)
    
    return True 