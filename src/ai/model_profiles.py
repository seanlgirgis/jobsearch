"""Validated, credential-free model profiles and machine-local selection."""

from __future__ import annotations

import json
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
PROFILE_NAME = re.compile(r"[a-z][a-z0-9_-]{0,47}\Z")
Provider = Literal["openrouter", "xai", "openai"]
ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"]


class ProfileError(ValueError):
    """A safe configuration error that does not echo file contents."""


class ModelTarget(BaseModel):
    """Capabilities must describe the exact model selected by the operator."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    provider: Provider
    model: str | None = Field(default=None, min_length=1, max_length=200)
    supports_json_schema: bool = False
    supports_temperature: bool = True
    token_parameter: Literal["max_tokens", "max_completion_tokens"] | None = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str | None) -> str | None:
        if value is not None and (
            any(char.isspace() or ord(char) < 32 for char in value)
            or value.startswith(("sk-", "xai-"))
        ):
            raise ValueError("Model must be a model ID, never a credential.")
        return value


class ModelProfile(BaseModel):
    """Policy and an ordered primary/fallback list; no artifact side effects."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    description: str = Field(default="", max_length=500)
    primary: ModelTarget
    fallbacks: list[ModelTarget] = Field(default_factory=list, max_length=5)
    temperature: float | None = Field(default=0.2, ge=0, le=2, allow_inf_nan=False)
    max_output_tokens: int = Field(default=1500, gt=0)
    reasoning_effort: ReasoningEffort | None = None
    structured_output: Literal["required", "optional", "off"] = "optional"
    allow_artifacts: bool = False

    @property
    def targets(self) -> tuple[ModelTarget, ...]:
        return (self.primary, *self.fallbacks)


class ProfileConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    version: Literal[1]
    active_profile: str
    profiles: dict[str, ModelProfile]


def _read_json(path: Path, *, optional: bool = False) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        if optional:
            return {}
        raise ProfileError("Profile example config is missing.") from None
    except (OSError, UnicodeError, ValueError):
        raise ProfileError(
            "Cannot read profile config; check permissions and JSON syntax."
        ) from None
    if not isinstance(value, dict):
        raise ProfileError("Profile config must be a JSON object.")
    return value


def _merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Merge object fields; replace lists, including the whole fallback list."""
    merged = deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def load_profiles(config_dir: Path = CONFIG_DIR) -> ProfileConfig:
    """Read the example and optional local overlay without loading .env or networking."""
    config_dir = Path(config_dir)
    data = _merge(
        _read_json(config_dir / "model_profiles.example.json"),
        _read_json(config_dir / "model_profiles.local.json", optional=True),
    )
    try:
        config = ProfileConfig.model_validate(data)
    except ValidationError:
        raise ProfileError(
            "Invalid profile config: check provider, model, capability flags, token budget, "
            "and output policy. Unknown fields and credentials are not allowed."
        ) from None
    if not config.profiles or any(not PROFILE_NAME.fullmatch(name) for name in config.profiles):
        raise ProfileError(
            "Profile names must be lowercase letters, digits, underscores or dashes."
        )
    if config.active_profile not in config.profiles:
        raise ProfileError(
            "Active profile is absent. Use model_profile.py list to see available names."
        )
    return config


def get_profile(config: ProfileConfig, name: str | None = None) -> ModelProfile:
    selected = config.active_profile if name is None else name
    if selected not in config.profiles:
        raise ProfileError("Profile is absent. Use model_profile.py list to see available names.")
    return config.profiles[selected]


def select_profile(name: str, config_dir: Path = CONFIG_DIR) -> ModelProfile:
    """Atomically update only the local selection, preserving local model settings."""
    config_dir = Path(config_dir)
    config = load_profiles(config_dir)
    profile = get_profile(config, name)
    path = config_dir / "model_profiles.local.json"
    local = _read_json(path, optional=True)
    local["active_profile"] = name
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=config_dir,
            prefix=".model_profiles-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(local, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
        os.replace(temp_path, path)
    except (OSError, ValueError):
        raise ProfileError(
            "Cannot save local profile selection; check config directory permissions."
        ) from None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    return profile
