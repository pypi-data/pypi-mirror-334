"""Configuration management for HostSpace CLI."""
import os
from pathlib import Path
from typing import Dict, Any, Optional, Literal

import yaml

CONFIG_DIR = Path.home() / ".hostspace"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

EnvironmentType = Literal["production", "development"]

DEFAULT_CONFIG = {
    "environment": "production",
    "environments": {
        "production": {
            "api_endpoint": "https://api.hostspace.cloud",
        },
        "development": {
            "api_endpoint": "https://aether-api-dev.hostspacecloud.com",
        }
    },
    "auth": {
        "api_key": None,
    },
    "providers": {
        "default": "contabo",
        "regions": [],
    },
    "output": {
        "format": "table",
        "color": True,
    },
}

class Config:
    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True)
        
        if not CONFIG_FILE.exists():
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)
            return config or DEFAULT_CONFIG.copy()
        except Exception:
            return DEFAULT_CONFIG.copy()

    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f)
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self._save_config(self._config)

    def get_api_key(self) -> Optional[str]:
        """Get API key from config."""
        return self._config.get("auth", {}).get("api_key")

    def set_api_key(self, api_key: str) -> None:
        """Set API key in config."""
        if "auth" not in self._config:
            self._config["auth"] = {}
        self._config["auth"]["api_key"] = api_key
        self._save_config(self._config)

    def get_environment(self) -> EnvironmentType:
        """Get current environment."""
        return self._config.get("environment", "production")

    def set_environment(self, env: EnvironmentType) -> None:
        """Set current environment."""
        if env not in self._config.get("environments", {}):
            raise ValueError(f"Unknown environment: {env}")
        self._config["environment"] = env
        self._save_config(self._config)

    def get_endpoint(self) -> str:
        """Get API endpoint for current environment."""
        env = self.get_environment()
        return self._config.get("environments", {}).get(env, {}).get(
            "api_endpoint", 
            DEFAULT_CONFIG["environments"][env]["api_endpoint"]
        )

config = Config()
