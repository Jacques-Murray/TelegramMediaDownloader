"""Media downloading functionality."""

import logging
from pathlib import Path
from typing import Any, Optional

from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

from ..models.media_info import MediaInfo
from ..protocols.file_namer import FileNamer
from ..protocols.media_filter import MediaFilter
from .connection import TelegramConnection


class MediaDownloader:
    """Handles media downloading operations."""

    def __init__(
        self,
        connection: TelegramConnection,
        download_path: Path,
        media_filter: MediaFilter,
        file_namer: FileNamer,
    ) -> None:
        """
        Initialize media downloader.

        Args:
            connection: Telegram connection instance
            download_path: Base path for downloads
            media_filter: Media filtering strategy
            file_namer: File naming strategy
        """
        self.connection = connection
        self.download_path = download_path
        self.media_filter = media_filter
        self.file_namer = file_namer
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure download path exists
        self.download_path.mkdir(parents=True, exist_ok=True)

    async def download_media_from_message(
        self, message: Any, channel_name: str
    ) -> Optional[MediaInfo]:
        """
        Download media from a single message.

        Args:
            message: Telegram message object
            channel_name: Name of the channel

        Returns:
            MediaInfo object if successful, None if failed
        """
        try:
            # Check if we should download this media
            if not self.media_filter.should_download(message):
                self.logger.debug(f"Skipping message {message.id} - filtered out")
                return None

            # Create channel-specific directory
            channel_dir = self.download_path / self._sanitize_channel_name(channel_name)
            channel_dir.mkdir(exist_ok=True)

            # Generate filename
            filename = self.file_namer.generate_filename(message, channel_name)
            filepath = channel_dir / filename

            # Check if file already exists
            if filepath.exists():
                self.logger.info(f"File already exists: {filename}")
                return MediaInfo(
                    message_id=message.id,
                    channel_name=channel_name,
                    filename=filename,
                    filepath=filepath,
                    date=message.date,
                    text=message.text,
                    mime_type=self._get_mime_type(message),
                )

            # Download the file
            self.logger.info(f"Downloading: {filename}")
            client = self.connection.get_client()

            downloaded_file = await client.download_media(message, file=str(filepath))

            if not downloaded_file:
                self.logger.error(f"Failed to download message {message.id}")
                return None

            # Create media info
            media_info = MediaInfo(
                message_id=message.id,
                channel_name=channel_name,
                filename=filename,
                filepath=filepath,
                date=message.date,
                text=message.text,
                mime_type=self._get_mime_type(message),
                file_size=filepath.stat().st_size if filepath.exists() else None,
            )

            # Save message metadata
            await self._save_metadata(media_info)

            self.logger.info(f"Successfully downloaded: {filename}")
            return media_info

        except Exception as e:
            self.logger.error(f"Error downloading media from message {message.id}: {e}")
            return None

    def _sanitize_channel_name(self, name: str) -> str:
        """
        Sanitize channel name for filesystem use.

        Args:
            name: Original channel name

        Returns:
            Sanitized name safe for filesystem
        """
        # Keep only safe characters
        safe_chars = []
        for char in name:
            if char.isalnum() or char in (" ", "-", "_"):
                safe_chars.append(char)
            else:
                safe_chars.append("_")

        safe_name = "".join(safe_chars).replace(" ", "_")

        # Clean up multiple underscores
        while "__" in safe_name:
            safe_name = safe_name.replace("__", "_")

        # Trim and limit length
        safe_name = safe_name.strip("_")[:100]

        return safe_name or "Unknown_Channel"

    def _get_mime_type(self, message: Any) -> Optional[str]:
        """
        Get MIME type from message media.

        Args:
            message: Telegram message object

        Returns:
            MIME type string or None
        """
        if isinstance(message.media, MessageMediaDocument):
            return message.media.document.mime_type
        elif isinstance(message.media, MessageMediaPhoto):
            return "image/jpeg"
        return None

    async def _save_metadata(self, media_info: MediaInfo) -> None:
        """
        Save message metadata to accompanying text file.

        Args:
            media_info: MediaInfo object with file details
        """
        try:
            info_file = media_info.filepath.with_suffix(".txt")

            with open(info_file, "w", encoding="utf-8") as f:
                f.write(f"Message ID: {media_info.message_id}\n")
                f.write(f"Channel: {media_info.channel_name}\n")
                f.write(f"Date: {media_info.date}\n")
                f.write(f"Filename: {media_info.filename}\n")
                f.write(f"MIME Type: {media_info.mime_type or 'Unknown'}\n")
                f.write(f"File Size: {media_info.file_size or 'Unknown'} bytes\n")
                f.write(f"Text: {media_info.text or 'No text content'}\n")

        except Exception as e:
            self.logger.warning(
                f"Failed to save metadata for {media_info.filename}: {e}"
            )
