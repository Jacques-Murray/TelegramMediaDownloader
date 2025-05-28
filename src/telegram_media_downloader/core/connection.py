"""Telegram connection management."""

import logging
from typing import Optional

from telethon import TelegramClient

from ..config.settings import TelegramConfig


class TelegramConnection:
    """Manages Telegram client connection lifecycle."""

    def __init__(self, config: TelegramConfig) -> None:
        """
        Initialize connection manager.

        Args:
            config: Telegram configuration
        """
        self.config = config
        self.client: Optional[TelegramClient] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    async def connect(self) -> None:
        """
        Establish connection to Telegram.

        Raises:
            RuntimeError: If connection fails
        """
        try:
            self.client = TelegramClient(
                self.config.session_name, self.config.api_id, self.config.api_hash
            )
            await self.client.start(phone=self.config.phone_number)
            self.logger.info("Successfully connected to Telegram")
        except Exception as e:
            self.logger.error(f"Failed to connect to Telegram: {e}")
            raise RuntimeError(f"Telegram connection failed: {e}") from e

    async def disconnect(self) -> None:
        """Close connection to Telegram."""
        if self.client:
            try:
                await self.client.disconnect()
                self.logger.info("Disconnected from Telegram")
            except Exception as e:
                self.logger.warning(f"Error during disconnect: {e}")
            finally:
                self.client = None

    def get_client(self) -> TelegramClient:
        """
        Get the Telegram client instance.

        Returns:
            Active TelegramClient instance

        Raises:
            RuntimeError: If client is not connected
        """
        if not self.client:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self.client is not None and self.client.is_connected()

    async def __aenter__(self) -> "TelegramConnection":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.disconnect()
