"""Video-only media filter implementation."""

from telethon.tl.types import MessageMediaDocument

from ..protocols.telegram_message import TelegramMessage


class VideoOnlyFilter:
    """Filter that only downloads video files."""

    def should_download(self, message: TelegramMessage) -> bool:
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
