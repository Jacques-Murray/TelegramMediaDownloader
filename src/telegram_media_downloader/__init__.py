"""
Telegram Media Downloader

A modern, object-oriented Python application for downloading images and videos
from unread messages in Telegram channels.
"""

__version__ = "1.0.0"
__author__ = "Jacques Murray"
__email__ = "jacquesmmurray@gmail.com"

# Core exports
from .config.settings import TelegramConfig
from .core.channel_manager import ChannelManager
from .core.connection import TelegramConnection
from .core.downloader import TelegramMediaDownloader
from .core.media_downloader import MediaDownloader

# Filter exports
from .filters.default_filter import DefaultMediaFilter
from .filters.image_filter import ImageOnlyFilter
from .filters.video_filter import VideoOnlyFilter
from .models.channel_stats import ChannelStats
from .models.download_session import DownloadSession

# Model exports
from .models.media_info import MediaInfo
from .namers.channel_prefix_namer import ChannelPrefixNamer

# Namer exports
from .namers.timestamp_namer import TimestampFileNamer
from .protocols.file_namer import FileNamer

# Protocol exports
from .protocols.media_filter import MediaFilter
from .utils.helpers import print_session_summary

# Utility exports
from .utils.logging import setup_logging

__all__ = [
    # Core
    "TelegramConfig",
    "TelegramMediaDownloader",
    "TelegramConnection",
    "ChannelManager",
    "MediaDownloader",
    # Models
    "MediaInfo",
    "ChannelStats",
    "DownloadSession",
    # Protocols
    "MediaFilter",
    "FileNamer",
    # Filters
    "DefaultMediaFilter",
    "VideoOnlyFilter",
    "ImageOnlyFilter",
    # Namers
    "TimestampFileNamer",
    "ChannelPrefixNamer",
    # Utils
    "setup_logging",
    "print_session_summary",
]
