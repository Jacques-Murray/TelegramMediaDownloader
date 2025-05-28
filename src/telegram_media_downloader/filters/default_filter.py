"""Default media filter implementation."""

from typing import Any

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class DefaultMediaFilter:
    """Default media filter - downloads images and videos."""
    
    def should_download(self, message: Any) -> bool:
        """
        Check if message contains downloadable media (images or videos).
        
        Args:
            message: Telegram message object
            
        Returns:
            True if message contains image or video media
        """
        if not message.media:
            return False
        
        # Check for photos
        if isinstance(message.media, MessageMediaPhoto):
            return True
        
        # Check for documents (videos, files, etc.)
        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document
            if document.mime_type:
                return (
                    document.mime_type.startswith('image/') or 
                    document.mime_type.startswith('video/')
                )
        
        return False