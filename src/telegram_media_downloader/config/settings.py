"""Configuration management for Telegram Media Downloader."""

import os
from pathlib import Path
from typing import List

import yaml


class TelegramConfig:
    """Configuration for Telegram connection."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone_number: str,
        session_name: str = "telegram_session",
    ) -> None:
        """
        Initialize Telegram configuration.

        Args:
            api_id: Telegram API ID from https://my.telegram.org/apps
            api_hash: Telegram API hash from https://my.telegram.org/apps
            phone_number: Phone number with country code (e.g., +1234567890)
            session_name: Name for the session file
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_name = session_name

    @classmethod
    def from_env(cls) -> "TelegramConfig":
        """
        Create configuration from environment variables or config.yaml if present.
        """
        config_path = Path("config.yaml")
        if config_path.exists():
            return cls.from_yaml(config_path)
        return cls(
            api_id=int(os.getenv("TELEGRAM_API_ID", "0")),
            api_hash=os.getenv("TELEGRAM_API_HASH", ""),
            phone_number=os.getenv("TELEGRAM_PHONE", ""),
            session_name=os.getenv("TELEGRAM_SESSION", "telegram_session"),
        )

    @classmethod
    def from_yaml(cls, path: Path) -> "TelegramConfig":
        """
        Create configuration from a YAML file.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(
            api_id=int(data.get("api_id", 0)),
            api_hash=data.get("api_hash", ""),
            phone_number=data.get("phone_number", ""),
            session_name=data.get("session_name", "telegram_session"),
        )

    def validate(self) -> List[str]:
        """
        Validate configuration and return list of errors.

        Returns:
            List of validation error messages
        """
        errors: List[str] = []

        if not self.api_id or self.api_id == 0:
            errors.append("API_ID is required and must be non-zero")

        if not self.api_hash:
            errors.append("API_HASH is required")

        if not self.phone_number:
            errors.append("PHONE_NUMBER is required")
        elif not self.phone_number.startswith("+"):
            errors.append("PHONE_NUMBER must include country code (e.g., +1234567890)")

        if not self.session_name:
            errors.append("SESSION_NAME cannot be empty")

        return errors

    def __repr__(self) -> str:
        """String representation (hiding sensitive data)."""
        return (
            f"TelegramConfig("
            f"api_id={self.api_id}, "
            f"phone_number={self.phone_number[:3]}*****, "
            f"session_name='{self.session_name}'"
            f")"
        )
