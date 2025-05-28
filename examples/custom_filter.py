"""Custom filter example - only download videos over 10MB."""

import asyncio

from telethon.tl.types import MessageMediaDocument

from telegram_media_downloader import TelegramConfig, TelegramMediaDownloader


class LargeVideoFilter:
    """Filter that only downloads large video files."""

    def __init__(self, min_size_mb: float = 10.0):
        self.min_size_bytes = int(min_size_mb * 1024 * 1024)

    def should_download(self, message) -> bool:
        """Check if message contains large video."""
        if not message.media:
            return False

        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document

            # Check if it's a video
            if not (document.mime_type and document.mime_type.startswith("video/")):
                return False

            # Check file size
            if hasattr(document, "size") and document.size >= self.min_size_bytes:
                return True

        return False


async def main():
    """Custom filter example."""
    print("🎬 Large Video Downloader Example")

    config = TelegramConfig.from_env()

    if config.validate():
        print("Please set your Telegram credentials in environment variables.")
        return

    # Use custom filter for large videos only
    large_video_filter = LargeVideoFilter(min_size_mb=10.0)

    async with TelegramMediaDownloader(
        config=config, media_filter=large_video_filter, download_path="large_videos"
    ) as downloader:

        print("🔍 Looking for videos larger than 10MB...")
        session = await downloader.download_all_unread_media()

        print(f"🎥 Downloaded {session.total_downloaded} large videos")

        # Show file details
        for stats in session.channel_stats:
            if stats.downloaded_count > 0:
                print(f"   {stats.name}: {stats.downloaded_count} videos")


if __name__ == "__main__":
    asyncio.run(main())
