from datetime import datetime

from telegram_media_downloader.namers.channel_prefix_namer import ChannelPrefixNamer


class DummyMessage:
    def __init__(self, channel_name: str, filename: str):
        self.id = 1
        self.date = datetime.now()
        self.text: str | None = "test"
        self.chat = type("Chat", (), {"title": channel_name})
        self.media = None


def test_channel_prefix_namer():
    namer = ChannelPrefixNamer()
    msg = DummyMessage("MyChannel", "file.jpg")
    name = namer.generate_filename(msg, "MyChannel")
    assert name.startswith("MyChannel_")
    assert name.endswith(".bin") 