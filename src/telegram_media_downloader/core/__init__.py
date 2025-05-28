"""Core functionality module."""

from .connection import TelegramConnection
from .channel_manager import ChannelManager
from .media_downloader import MediaDownloader
from .downloader import TelegramMediaDownloader

__all__ = [
    'TelegramConnection',
    'ChannelManager',
    'MediaDownloader',
    'TelegramMediaDownloader'
]