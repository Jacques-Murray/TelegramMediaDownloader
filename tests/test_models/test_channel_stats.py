from telegram_media_downloader.models.channel_stats import ChannelStats


def test_channel_stats_repr():
    stats = ChannelStats(name="TestChannel", unread_count=2, media_count=10, downloaded_count=5, errors=["err1"])
    s = str(stats)
    assert "TestChannel" in s
    assert "downloaded=5" in s
    assert "errors=1" in s 