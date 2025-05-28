"""Basic usage example for Telegram Media Downloader."""

import asyncio
import os

from telegram_media_downloader import TelegramConfig, TelegramMediaDownloader


async def main():
    """Basic usage example."""
    print("🚀 Basic Telegram Media Downloader Example")

    # Create config from environment variables
    config = TelegramConfig(
        api_id=int(os.getenv("TELEGRAM_API_ID", "0")),
        api_hash=os.getenv("TELEGRAM_API_HASH", ""),
        phone_number=os.getenv("TELEGRAM_PHONE", ""),
    )

    # Validate config
    errors = config.validate()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return

    # Use context manager for automatic cleanup
    async with TelegramMediaDownloader(
        config=config, download_path="basic_downloads"
    ) as downloader:

        print("📡 Connecting to Telegram...")

        # Download all unread media
        session = await downloader.download_all_unread_media(mark_as_read=True)

        # Print summary
        print(f"\n✅ Download completed!")
        print(f"📊 Processed {session.total_channels} channels")
        print(f"📥 Downloaded {session.total_downloaded} files")
        print(f"⏱️  Duration: {session.duration}")

        # Show per-channel results
        if session.channels_with_downloads:
            print(f"\n📁 Files downloaded by channel:")
            for stats in session.channels_with_downloads:
                print(f"   {stats.name}: {stats.downloaded_count} files")


if __name__ == "__main__":
    asyncio.run(main())
