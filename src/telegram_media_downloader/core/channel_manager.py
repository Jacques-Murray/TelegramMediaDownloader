"""Channel and message management."""

import logging
from typing import Any, List

from .connection import TelegramConnection


class ChannelManager:
    """Manages Telegram channels and messages."""

    def __init__(self, connection: TelegramConnection) -> None:
        """
        Initialize channel manager.

        Args:
            connection: Telegram connection instance
        """
        self.connection = connection
        self.logger = logging.getLogger(self.__class__.__name__)

    async def get_all_channels(self) -> List[Any]:
        """
        Get all channels the user is subscribed to.

        Returns:
            List of channel dialog objects
        """
        try:
            client = self.connection.get_client()
            channels = []

            async for dialog in client.iter_dialogs():
                if dialog.is_channel:
                    channels.append(dialog)

            self.logger.info(f"Found {len(channels)} channels")
            return channels

        except Exception as e:
            self.logger.error(f"Error getting channels: {e}")
            raise

    async def get_unread_messages(self, channel: Any) -> List[Any]:
        """
        Get unread messages from a specific channel.

        Args:
            channel: Channel dialog object

        Returns:
            List of unread message objects
        """
        try:
            unread_count = channel.unread_count

            if unread_count == 0:
                self.logger.debug(f"No unread messages in {channel.title}")
                return []

            self.logger.info(f"Found {unread_count} unread messages in {channel.title}")

            client = self.connection.get_client()
            messages = []

            async for message in client.iter_messages(
                channel.entity, limit=unread_count
            ):
                messages.append(message)

            return messages

        except Exception as e:
            self.logger.error(
                f"Error getting unread messages from {channel.title}: {e}"
            )
            return []

    async def mark_messages_as_read(self, channel: Any, messages: List[Any]) -> None:
        """
        Mark messages as read in a channel.

        Args:
            channel: Channel dialog object
            messages: List of message objects to mark as read
        """
        try:
            if not messages:
                return

            client = self.connection.get_client()
            await client.send_read_acknowledge(channel.entity, messages[0])

            self.logger.info(
                f"Marked {len(messages)} messages as read in {channel.title}"
            )

        except Exception as e:
            self.logger.error(f"Error marking messages as read in {channel.title}: {e}")

    async def get_channel_info(self, channel: Any) -> dict:
        """
        Get detailed information about a channel.

        Args:
            channel: Channel dialog object

        Returns:
            Dictionary with channel information
        """
        try:
            return {
                "id": channel.entity.id,
                "title": channel.title,
                "username": getattr(channel.entity, "username", None),
                "unread_count": channel.unread_count,
                "is_channel": channel.is_channel,
                "is_group": channel.is_group,
                "is_user": channel.is_user,
            }
        except Exception as e:
            self.logger.error(f"Error getting channel info: {e}")
            return {"title": "Unknown", "error": str(e)}
