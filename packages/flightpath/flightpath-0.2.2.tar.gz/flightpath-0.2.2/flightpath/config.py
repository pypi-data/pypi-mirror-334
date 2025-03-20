import json
from pathlib import Path
from typing import Optional, Dict
import logging

# Constants
THROTTLE_DURATION_SECONDS = 3
CONFIG_FILE = Path.home() / ".config" / "flightpath" / "config.json"


def load_config() -> Dict[str, str]:
    """Load configuration from the config file if it exists."""
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        logging.debug("Config file not found at %s", CONFIG_FILE)
        return {}
    except json.JSONDecodeError:
        logging.warning("Failed to parse config file at %s - invalid JSON", CONFIG_FILE)
        return {}


def get_auth_config() -> Dict[str, Optional[str]]:
    """Get authentication configuration with defaults."""
    config = load_config()
    return {
        "username": config.get("username"),
        "password": config.get("password"),
        "baseurl": config.get("baseurl"),
    }
