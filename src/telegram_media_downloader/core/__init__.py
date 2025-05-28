"""Core functionality module."""

from .channel_manager import ChannelManager
from .connection import TelegramConnection
from .downloader import TelegramMediaDownloader
from .media_downloader import MediaDownloader

__all__ = [
    "TelegramConnection",
    "ChannelManager",
    "MediaDownloader",
    "TelegramMediaDownloader",
]
