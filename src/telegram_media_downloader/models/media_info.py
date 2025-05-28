"""Data models for media information."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class MediaInfo:
    """Information about downloaded media file."""
    
    message_id: int
    channel_name: str
    filename: str
    filepath: Path
    date: datetime
    text: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    
    @property
    def file_exists(self) -> bool:
        """Check if the downloaded file exists."""
        return self.filepath.exists()
    
    @property
    def actual_file_size(self) -> Optional[int]:
        """Get actual file size from filesystem."""
        if self.file_exists:
            return self.filepath.stat().st_size
        return None
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"MediaInfo(message_id={self.message_id}, "
            f"channel='{self.channel_name}', "
            f"filename='{self.filename}', "
            f"date={self.date.strftime('%Y-%m-%d %H:%M:%S')})"
        )