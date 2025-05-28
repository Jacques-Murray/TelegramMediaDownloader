"""Channel prefix file naming implementation."""

from pathlib import Path
from typing import Any

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class ChannelPrefixNamer:
    """File namer that prefixes filenames with channel name."""
    
    def generate_filename(self, message: Any, channel_name: str) -> str:
        """
        Generate filename with channel name prefix.
        
        Format: ChannelName_YYYYMMDD_HHMMSS_msgID.extension
        
        Args:
            message: Telegram message object
            channel_name: Name of the channel
            
        Returns:
            Generated filename with channel prefix and extension
        """
        # Sanitize channel name for filesystem
        safe_channel = self._sanitize_name(channel_name)
        
        # Generate timestamp
        timestamp = message.date.strftime("%Y%m%d_%H%M%S")
        
        # Get file extension
        extension = self._get_file_extension(message)
        
        return f"{safe_channel}_{timestamp}_msg{message.id}{extension}"
    
    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize channel name for filesystem use.
        
        Args:
            name: Original channel name
            
        Returns:
            Sanitized name safe for filesystem
        """
        # Keep only alphanumeric characters and common safe symbols
        safe_chars = []
        for char in name:
            if char.isalnum() or char in (' ', '-', '_'):
                safe_chars.append(char)
            else:
                safe_chars.append('_')
        
        # Join and clean up multiple underscores/spaces
        safe_name = ''.join(safe_chars)
        safe_name = safe_name.replace(' ', '_')
        
        # Remove multiple consecutive underscores
        while '__' in safe_name:
            safe_name = safe_name.replace('__', '_')
        
        # Trim and limit length
        safe_name = safe_name.strip('_')[:50]
        
        return safe_name or 'Unknown'
    
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
                    # Handle common MIME type variations
                    if mime_ext == 'jpeg':
                        return '.jpg'
                    elif mime_ext == 'png':
                        return '.png'
                    elif mime_ext == 'gif':
                        return '.gif'
                    elif mime_ext == 'webp':
                        return '.webp'
                    else:
                        return f'.{mime_ext}'
                elif document.mime_type.startswith('video/'):
                    mime_ext = document.mime_type.split('/')[-1]
                    # Handle common video MIME types
                    if mime_ext == 'mp4':
                        return '.mp4'
                    elif mime_ext == 'avi':
                        return '.avi'
                    elif mime_ext == 'mov':
                        return '.mov'
                    elif mime_ext == 'mkv':
                        return '.mkv'
                    elif mime_ext == 'webm':
                        return '.webm'
                    else:
                        return f'.{mime_ext}'
                elif document.mime_type.startswith('audio/'):
                    mime_ext = document.mime_type.split('/')[-1]
                    return f'.{mime_ext}'
            
            # Try to get extension from file name in attributes
            for attr in document.attributes:
                if hasattr(attr, 'file_name') and attr.file_name:
                    file_extension = Path(attr.file_name).suffix
                    if file_extension:
                        return file_extension
        
        # Default extension for unknown types
        return '.bin'