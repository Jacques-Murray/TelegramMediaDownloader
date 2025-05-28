"""Data models for channel statistics."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ChannelStats:
    """Statistics for a single channel processing session."""

    name: str
    unread_count: int = 0
    media_count: int = 0
    downloaded_count: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.media_count == 0:
            return 100.0
        return (self.downloaded_count / self.media_count) * 100

    @property
    def has_errors(self) -> bool:
        """Check if there were any errors during processing."""
        return len(self.errors) > 0

    @property
    def error_count(self) -> int:
        """Get number of errors."""
        return len(self.errors)

    def add_error(self, error: str) -> None:
        """Add an error message to the stats."""
        self.errors.append(error)

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"ChannelStats(name='{self.name}', "
            f"unread={self.unread_count}, "
            f"media={self.media_count}, "
            f"downloaded={self.downloaded_count}, "
            f"success_rate={self.success_rate:.1f}%, "
            f"errors={self.error_count})"
        )
