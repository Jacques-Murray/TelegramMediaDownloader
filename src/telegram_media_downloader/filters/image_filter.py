"""Image-only media filter implementation."""

from typing import Any

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class ImageOnlyFilter:
    """Filter that only downloads image files."""
    
    def should_download(self, message: Any) -> bool:
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
                return document.mime_type.startswith('image/')
        
        return False