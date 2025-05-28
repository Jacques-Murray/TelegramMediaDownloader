from datetime import datetime

from telethon.tl.types import MessageMediaPhoto  # type: ignore

from telegram_media_downloader.filters.image_filter import ImageOnlyFilter


class DummyPhoto:
    pass

class DummyMessage:
    def __init__(self, has_photo: bool):
        self.media = MessageMediaPhoto() if has_photo else None
        self.id = 1
        self.date = datetime.now()
        self.text: str | None = None


def test_image_only_filter_accepts_photo():
    filter = ImageOnlyFilter()
    msg = DummyMessage(True)
    assert filter.should_download(msg)

def test_image_only_filter_rejects_non_photo():
    filter = ImageOnlyFilter()
    msg = DummyMessage(False)
    assert not filter.should_download(msg) 