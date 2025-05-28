from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.telegram_media_downloader.config.settings import TelegramConfig
from src.telegram_media_downloader.core.downloader import TelegramMediaDownloader


@pytest.fixture
def config():
    return TelegramConfig(api_id=123, api_hash="abc", phone_number="+1234567890")


@pytest.mark.asyncio
async def test_download_all_unread_media_success(config):
    with patch(
        "src.telegram_media_downloader.core.downloader.TelegramConnection"
    ) as MockConn, patch(
        "src.telegram_media_downloader.core.downloader.ChannelManager"
    ) as MockChanMgr, patch(
        "src.telegram_media_downloader.core.downloader.MediaDownloader"
    ) as MockMediaDownloader:
        mock_conn = MockConn.return_value
        mock_chan_mgr = MockChanMgr.return_value
        mock_media_downloader = MockMediaDownloader.return_value
        mock_chan_mgr.get_all_channels = AsyncMock(
            return_value=[MagicMock(title="TestChannel")]
        )
        mock_chan_mgr.get_unread_messages = AsyncMock(return_value=[MagicMock(id=1)])
        mock_media_downloader.download_media_from_message = AsyncMock(return_value=True)
        mock_chan_mgr.mark_messages_as_read = AsyncMock()
        downloader = TelegramMediaDownloader(config=config)
        async with downloader:
            session = await downloader.download_all_unread_media()
        assert session.total_downloaded == 1
        assert session.total_channels == 1
        assert not session.errors


@pytest.mark.asyncio
async def test_download_all_unread_media_error(config):
    with patch(
        "src.telegram_media_downloader.core.downloader.TelegramConnection"
    ) as MockConn, patch(
        "src.telegram_media_downloader.core.downloader.ChannelManager"
    ) as MockChanMgr, patch(
        "src.telegram_media_downloader.core.downloader.MediaDownloader"
    ) as MockMediaDownloader:
        mock_conn = MockConn.return_value
        mock_chan_mgr = MockChanMgr.return_value
        mock_media_downloader = MockMediaDownloader.return_value
        mock_chan_mgr.get_all_channels = AsyncMock(side_effect=Exception("fail"))
        downloader = TelegramMediaDownloader(config=config)
        async with downloader:
            session = await downloader.download_all_unread_media()
        assert session.total_downloaded == 0
        assert session.errors


@pytest.mark.asyncio
async def test_download_from_specific_channels(config):
    with patch(
        "src.telegram_media_downloader.core.downloader.TelegramConnection"
    ) as MockConn, patch(
        "src.telegram_media_downloader.core.downloader.ChannelManager"
    ) as MockChanMgr, patch(
        "src.telegram_media_downloader.core.downloader.MediaDownloader"
    ) as MockMediaDownloader:
        mock_conn = MockConn.return_value
        mock_chan_mgr = MockChanMgr.return_value
        mock_media_downloader = MockMediaDownloader.return_value
        mock_chan_mgr.get_all_channels = AsyncMock(
            return_value=[MagicMock(title="A"), MagicMock(title="B")]
        )
        mock_chan_mgr.get_unread_messages = AsyncMock(return_value=[MagicMock(id=1)])
        mock_media_downloader.download_media_from_message = AsyncMock(return_value=True)
        mock_chan_mgr.mark_messages_as_read = AsyncMock()
        downloader = TelegramMediaDownloader(config=config)
        async with downloader:
            session = await downloader.download_from_specific_channels(["A"])
        assert session.total_channels == 1
        assert session.total_downloaded == 1
