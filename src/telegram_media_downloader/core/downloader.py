"""Main downloader orchestrator."""

import logging
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import Any, Optional

from ..config.settings import TelegramConfig
from ..filters.default_filter import DefaultMediaFilter
from ..models.channel_stats import ChannelStats
from ..models.download_session import DownloadSession
from ..namers.timestamp_namer import TimestampFileNamer
from ..protocols.file_namer import FileNamer
from ..protocols.media_filter import MediaFilter
from ..utils.logging import get_logger
from .channel_manager import ChannelManager
from .connection import TelegramConnection
from .media_downloader import MediaDownloader


class TelegramMediaDownloader:
    """Main downloader orchestrator."""

    def __init__(
        self,
        config: TelegramConfig,
        download_path: str = "downloads",
        media_filter: Optional[MediaFilter] = None,
        file_namer: Optional[FileNamer] = None,
        fail_fast: bool = False,
    ) -> None:
        """
        Initialize the main downloader.

        Args:
            config: Telegram configuration
            download_path: Base path for downloads
            media_filter: Media filtering strategy (defaults to DefaultMediaFilter)
            file_namer: File naming strategy (defaults to TimestampFileNamer)
            fail_fast: Whether to fail fast on error
        """
        self.config = config
        self.download_path = Path(download_path)
        self.media_filter = media_filter or DefaultMediaFilter()
        self.file_namer = file_namer or TimestampFileNamer()
        self.logger = get_logger(self.__class__.__name__)
        self.fail_fast = fail_fast

        # Initialize core components
        self.connection = TelegramConnection(config)
        self.channel_manager = ChannelManager(self.connection)
        self.media_downloader = MediaDownloader(
            self.connection, self.download_path, self.media_filter, self.file_namer
        )

    async def __aenter__(self) -> "TelegramMediaDownloader":
        """Async context manager entry."""
        await self.connection.connect()
        return self

    async def __aexit__(self, exc_type: type, exc_val: Exception, exc_tb: Optional[TracebackType]) -> None:
        """Async context manager exit."""
        await self.connection.disconnect()

    async def download_all_unread_media(
        self, mark_as_read: bool = True
    ) -> DownloadSession:
        """
        Download media from all unread messages in all channels.

        Args:
            mark_as_read: Whether to mark messages as read after processing

        Returns:
            DownloadSession with summary information
        """
        start_time = datetime.now()
        session_errors: list[str] = []
        channel_stats: list[ChannelStats] = []

        try:
            self.logger.info("Starting download session")

            # Get all channels
            channels = await self.channel_manager.get_all_channels()
            self.logger.info(f"Found {len(channels)} channels to process")

            # Process each channel
            total_unread = 0
            total_media = 0
            total_downloaded = 0

            for channel in channels:
                try:
                    stats = await self._process_channel(channel, mark_as_read)
                    channel_stats.append(stats)

                    total_unread += stats.unread_count
                    total_media += stats.media_count
                    total_downloaded += stats.downloaded_count

                    if self.fail_fast and (stats.has_errors or stats.error_count > 0):
                        raise RuntimeError(f"Error in channel {getattr(channel, 'title', 'Unknown')}")

                except Exception as e:
                    error_msg = f"Failed to process channel {getattr(channel, 'title', 'Unknown')}: {e}"
                    self.logger.error(error_msg)
                    session_errors.append(error_msg)

                    # Add error stats for failed channel
                    channel_stats.append(
                        ChannelStats(
                            name=getattr(channel, "title", "Unknown"),
                            errors=[error_msg],
                        )
                    )
                    if self.fail_fast:
                        break

            end_time = datetime.now()

            session = DownloadSession(
                total_channels=len(channels),
                total_unread=total_unread,
                total_media=total_media,
                total_downloaded=total_downloaded,
                channel_stats=channel_stats,
                start_time=start_time,
                end_time=end_time,
                errors=session_errors,
            )

            self.logger.info(f"Download session completed: {session}")
            return session

        except Exception as e:
            error_msg = f"Download session failed: {e}"
            self.logger.error(error_msg)
            session_errors.append(error_msg)

            return DownloadSession(
                total_channels=0,
                total_unread=0,
                total_media=0,
                total_downloaded=0,
                channel_stats=list(channel_stats),
                start_time=start_time,
                end_time=datetime.now(),
                errors=list(session_errors),
            )

    async def _process_channel(self, channel, mark_as_read: bool) -> ChannelStats:
        """
        Process a single channel.

        Args:
            channel: Channel dialog object
            mark_as_read: Whether to mark messages as read

        Returns:
            ChannelStats object with processing results
        """
        channel_name = getattr(channel, "title", "Unknown")
        self.logger.info(f"Processing channel: {channel_name}")

        stats = ChannelStats(name=channel_name)

        try:
            # Get unread messages
            unread_messages = await self.channel_manager.get_unread_messages(channel)
            stats.unread_count = len(unread_messages)

            if not unread_messages:
                self.logger.info(f"No unread messages in {channel_name}")
                return stats

            # Filter messages with media
            media_messages = [
                msg for msg in unread_messages if self.media_filter.should_download(msg)
            ]
            stats.media_count = len(media_messages)

            self.logger.info(
                f"Found {len(media_messages)} media messages in {channel_name}"
            )

            # Download media from each message
            for message in media_messages:
                try:
                    media_info = (
                        await self.media_downloader.download_media_from_message(
                            message, channel_name
                        )
                    )
                    if media_info:
                        stats.downloaded_count += 1
                    else:
                        stats.add_error(f"Failed to download message {message.id}")

                except Exception as e:
                    error_msg = f"Error downloading message {message.id}: {e}"
                    self.logger.error(error_msg)
                    stats.add_error(error_msg)

            # Mark messages as read if requested
            if mark_as_read and unread_messages:
                await self.channel_manager.mark_messages_as_read(
                    channel, unread_messages
                )

            self.logger.info(f"Channel {channel_name} processed: {stats}")
            return stats

        except Exception as e:
            error_msg = f"Error processing channel {channel_name}: {e}"
            self.logger.error(error_msg)
            stats.add_error(error_msg)
            return stats

    async def download_from_specific_channels(
        self, channel_names: list[str], mark_as_read: bool = True
    ) -> DownloadSession:
        """
        Download media from specific channels only.

        Args:
            channel_names: List of channel names to process
            mark_as_read: Whether to mark messages as read

        Returns:
            DownloadSession with results
        """
        start_time = datetime.now()

        # Get all channels and filter by names
        all_channels = await self.channel_manager.get_all_channels()
        target_channels = [
            ch for ch in all_channels if getattr(ch, "title", "") in channel_names
        ]

        if not target_channels:
            self.logger.warning(f"No matching channels found for: {channel_names}")

        # Process filtered channels
        session_errors = []
        channel_stats = []
        total_unread = 0
        total_media = 0
        total_downloaded = 0

        for channel in target_channels:
            stats = await self._process_channel(channel, mark_as_read)
            channel_stats.append(stats)

            total_unread += stats.unread_count
            total_media += stats.media_count
            total_downloaded += stats.downloaded_count

        return DownloadSession(
            total_channels=len(target_channels),
            total_unread=total_unread,
            total_media=total_media,
            total_downloaded=total_downloaded,
            channel_stats=channel_stats,
            start_time=start_time,
            end_time=datetime.now(),
            errors=session_errors,
        )
