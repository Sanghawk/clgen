# clgen/config.py
import copy
import os
from pathlib import Path
from typing import Any, Dict, Optional

import click
import tomli
import tomli_w


class Config:
    DEFAULTS: Dict[str, Dict[str, Any]] = {
        "openai": {
            "key": None,
            "model": "gpt-4",
        },
    }

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
        self.config_dir = config_dir or (base / "clgen")
        self.config_file = self.config_dir / "config.toml"
        self._ensure_dir()
        self._data = self._load()

    def _ensure_dir(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _deep_merge(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> None:  # noqa: E501
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                self._deep_merge(base[k], v)
            else:
                base[k] = v

    def _load(self) -> Dict[str, Any]:
        if not self.config_file.exists():
            data = copy.deepcopy(self.DEFAULTS)
            self._save(data)
            return data

        try:
            with open(self.config_file, "rb") as f:
                user_cfg = tomli.load(f)
            data = copy.deepcopy(self.DEFAULTS)
            self._deep_merge(data, user_cfg)
            return data
        except Exception as e:
            click.echo(f"[!] Error loading config: {e}", err=True)
            return copy.deepcopy(self.DEFAULTS)

    def _save(self, data: Dict[str, Any]) -> None:
        # Convert None values to empty strings for TOML serialization
        def convert_none_to_empty(obj: Any) -> Any:
            if obj is None:
                return ""
            if isinstance(obj, dict):
                return {k: convert_none_to_empty(v) for k, v in obj.items()}
            return obj

        data_to_save = convert_none_to_empty(data)
        toml_str = tomli_w.dumps(data_to_save)
        self.config_file.write_text(toml_str)
        os.chmod(self.config_file, 0o600)

    # Public methods

    def save(self) -> None:
        """Persist current in-memory config (self._data)."""
        self._save(self._data)

    @property
    def openai_key(self) -> Optional[str]:
        key = self._data["openai"]["key"]
        return str(key) if key is not None else None

    @openai_key.setter
    def openai_key(self, value: str) -> None:
        self._data["openai"]["key"] = value
        self.save()

    @property
    def openai_model(self) -> str:
        return str(self._data["openai"]["model"])

    @openai_model.setter
    def openai_model(self, value: str) -> None:
        self._data["openai"]["model"] = value
        self.save()
