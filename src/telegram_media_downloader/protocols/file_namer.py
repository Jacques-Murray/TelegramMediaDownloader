"""Protocol definition for file naming strategies."""

from typing import Any, Protocol


class FileNamer(Protocol):
    """Protocol for file naming strategies."""

    def generate_filename(self, message: Any, channel_name: str) -> str:
        """
        Generate a filename for downloaded media.

        Args:
            message: Telegram message object
            channel_name: Name of the channel the message is from

        Returns:
            Generated filename including extension
        """
        ...
