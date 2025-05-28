"""Video-only media filter implementation."""

from typing import Any

from telethon.tl.types import MessageMediaDocument


class VideoOnlyFilter:
    """Filter that only downloads video files."""

    def should_download(self, message: Any) -> bool:
        """
        Check if message contains video media.

        Args:
            message: Telegram message object

        Returns:
            True if message contains video media
        """
        if not message.media:
            return False

        # Only check for video documents
        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document
            if document.mime_type:
                return document.mime_type.startswith("video/")

        return False
