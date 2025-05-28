"""Protocol definition for media filtering strategies."""

from typing import Any, Protocol


class MediaFilter(Protocol):
    """Protocol for media filtering strategies."""

    def should_download(self, message: Any) -> bool:
        """
        Determine if media from a message should be downloaded.

        Args:
            message: Telegram message object

        Returns:
            True if the media should be downloaded, False otherwise
        """
        ...
