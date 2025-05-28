"""Image-only media filter implementation."""

from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

from ..protocols.telegram_message import TelegramMessage


class ImageOnlyFilter:
    """Filter that only downloads image files."""

    def should_download(self, message: TelegramMessage) -> bool:
        """
        Check if message contains image media.

        Args:
            message: Telegram message object

        Returns:
            True if message contains image media
        """
        if not message.media:
            return False

        # Check for photos
        if isinstance(message.media, MessageMediaPhoto):
            return True

        # Check for image documents
        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document
            if document.mime_type:
                return document.mime_type.startswith("image/")

        return False
