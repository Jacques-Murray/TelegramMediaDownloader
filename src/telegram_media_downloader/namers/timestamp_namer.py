"""Timestamp-based file naming implementation."""

from pathlib import Path
from typing import Any

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class TimestampFileNamer:
    """File namer that uses timestamps and message IDs."""
    
    def generate_filename(self, message: Any, channel_name: str) -> str:
        """
        Generate filename using timestamp and message ID.
        
        Format: YYYYMMDD_HHMMSS_msgID.extension
        
        Args:
            message: Telegram message object
            channel_name: Name of the channel (not used in this implementation)
            
        Returns:
            Generated filename with extension
        """
        timestamp = message.date.strftime("%Y%m%d_%H%M%S")
        extension = self._get_file_extension(message)
        return f"{timestamp}_msg{message.id}{extension}"
    
    def _get_file_extension(self, message: Any) -> str:
        """
        Get appropriate file extension for the media.
        
        Args:
            message: Telegram message object
            
        Returns:
            File extension including the dot (e.g., '.jpg', '.mp4')
        """
        if isinstance(message.media, MessageMediaPhoto):
            return '.jpg'
        
        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document
            
            # Try to get extension from MIME type
            if document.mime_type:
                if document.mime_type.startswith('image/'):
                    mime_ext = document.mime_type.split('/')[-1]
                    return f'.{mime_ext}'
                elif document.mime_type.startswith('video/'):
                    mime_ext = document.mime_type.split('/')[-1]
                    return f'.{mime_ext}'
            
            # Try to get extension from file name in attributes
            for attr in document.attributes:
                if hasattr(attr, 'file_name') and attr.file_name:
                    return Path(attr.file_name).suffix
        
        # Default extension for unknown types
        return '.bin'