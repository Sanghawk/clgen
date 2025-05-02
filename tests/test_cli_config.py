import os
from pathlib import Path

import pytest
import tomli
from click.testing import CliRunner

from clgen.cli import cli


@pytest.fixture(autouse=True)
def isolate_config(monkeypatch, tmp_path):
    """
    Redirect XDG_CONFIG_HOME to a tmp dir so we don't
    touch the user's real config.
    """
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    yield


@pytest.fixture
def runner():
    return CliRunner()


def test_get_key_when_not_set(runner):
    # No key has been set yet → should inform the user
    result = runner.invoke(cli, ["config", "openai", "get-key"])
    assert result.exit_code == 0
    assert "No key set." in result.output


def test_set_and_get_key(runner):
    # 1) Set a new key
    key = "abcd1234"
    result = runner.invoke(cli, ["config", "openai", "set-key", key])
    assert result.exit_code == 0
    assert "Key saved." in result.output

    # 2) Getting it back should show only the last 4 chars, prefixed by ****
    result = runner.invoke(cli, ["config", "openai", "get-key"])
    assert result.exit_code == 0
    assert result.output.strip() == "****1234"

    # 3) Inspect the on-disk config to ensure it was written
    cfg_file = Path(os.getenv("XDG_CONFIG_HOME")) / "clgen" / "config.toml"
    with open(cfg_file, "rb") as f:
        data = tomli.load(f)
    assert data["openai"]["key"] == key


def test_get_model_default(runner):
    # Default model is 'gpt-4' per DEFAULTS
    result = runner.invoke(cli, ["config", "openai", "get-model"])
    assert result.exit_code == 0
    assert result.output.strip() == "gpt-4"


def test_set_and_get_model(runner):
    # 1) Change model
    model = "gpt-3.5-turbo"
    result = runner.invoke(cli, ["config", "openai", "set-model", model])
    assert result.exit_code == 0
    assert f"Model set to {model}" in result.output

    # 2) Confirm via CLI
    result = runner.invoke(cli, ["config", "openai", "get-model"])
    assert result.exit_code == 0
    assert result.output.strip() == model

    # 3) And ensure persistence on disk
    cfg_file = Path(os.getenv("XDG_CONFIG_HOME")) / "clgen" / "config.toml"
    with open(cfg_file, "rb") as f:
        data = tomli.load(f)
    assert data["openai"]["model"] == model
