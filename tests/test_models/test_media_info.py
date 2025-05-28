from datetime import datetime
from pathlib import Path

from telegram_media_downloader.models.media_info import MediaInfo


def test_media_info_repr():
    info = MediaInfo(
        message_id=1,
        channel_name="TestChannel",
        filename="file.jpg",
        filepath=Path("/tmp/file.jpg"),
        date=datetime.now(),
        text="desc",
        mime_type="image/jpeg",
        file_size=1234,
    )
    r = repr(info)
    assert "TestChannel" in r
    assert "file.jpg" in r 