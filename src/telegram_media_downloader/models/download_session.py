"""Data models for download session information."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

from .channel_stats import ChannelStats


@dataclass
class DownloadSession:
    """Summary of a complete download session."""

    total_channels: int
    total_unread: int
    total_media: int
    total_downloaded: int
    channel_stats: List[ChannelStats]
    start_time: datetime
    end_time: datetime
    errors: List[str] = field(default_factory=list)

    @property
    def duration(self) -> timedelta:
        """Get session duration."""
        return self.end_time - self.start_time

    @property
    def success_rate(self) -> float:
        """Calculate overall success rate as percentage."""
        if self.total_media == 0:
            return 100.0
        return (self.total_downloaded / self.total_media) * 100

    @property
    def channels_with_downloads(self) -> List[ChannelStats]:
        """Get channels that had successful downloads."""
        return [stats for stats in self.channel_stats if stats.downloaded_count > 0]

    @property
    def channels_with_errors(self) -> List[ChannelStats]:
        """Get channels that had errors."""
        return [stats for stats in self.channel_stats if stats.has_errors]

    @property
    def total_errors(self) -> int:
        """Get total number of errors (session + channel errors)."""
        channel_errors = sum(len(stats.errors) for stats in self.channel_stats)
        return len(self.errors) + channel_errors

    @property
    def average_files_per_channel(self) -> float:
        """Calculate average files downloaded per channel."""
        active_channels = len([s for s in self.channel_stats if s.downloaded_count > 0])
        if active_channels == 0:
            return 0.0
        return self.total_downloaded / active_channels

    def add_session_error(self, error: str) -> None:
        """Add a session-level error."""
        self.errors.append(error)

    def get_summary_dict(self) -> dict:
        """Get session summary as dictionary."""
        return {
            "duration": str(self.duration),
            "channels_processed": self.total_channels,
            "unread_messages": self.total_unread,
            "media_messages": self.total_media,
            "files_downloaded": self.total_downloaded,
            "success_rate": f"{self.success_rate:.1f}%",
            "channels_with_downloads": len(self.channels_with_downloads),
            "channels_with_errors": len(self.channels_with_errors),
            "total_errors": self.total_errors,
            "avg_files_per_channel": f"{self.average_files_per_channel:.1f}",
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"DownloadSession("
            f"duration={self.duration}, "
            f"channels={self.total_channels}, "
            f"downloaded={self.total_downloaded}, "
            f"success_rate={self.success_rate:.1f}%"
            f")"
        )
