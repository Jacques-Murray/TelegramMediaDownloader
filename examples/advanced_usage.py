"""Advanced usage example with multiple features."""

import asyncio
from pathlib import Path

from telegram_media_downloader import (
    ChannelPrefixNamer,
    ImageOnlyFilter,
    TelegramConfig,
    TelegramMediaDownloader,
    create_download_summary_file,
    print_session_summary,
)


async def main():
    """Advanced usage example."""
    print("🚀 Advanced Telegram Media Downloader Example")
    print("=" * 50)

    # Load config
    config = TelegramConfig.from_env()

    if config.validate():
        print("❌ Please configure your Telegram credentials first.")
        return

    # Setup custom components
    image_filter = ImageOnlyFilter()  # Only download images
    channel_namer = ChannelPrefixNamer()  # Prefix files with channel name

    async with TelegramMediaDownloader(
        config=config,
        media_filter=image_filter,
        file_namer=channel_namer,
        download_path="advanced_downloads",
    ) as downloader:

        print("🖼️  Downloading images only with channel prefixes...")

        # Download from all channels
        session = await downloader.download_all_unread_media(mark_as_read=False)

        # Print detailed summary
        print_session_summary(session)

        # Save summary to file
        summary_path = Path("advanced_downloads") / "session_report.txt"
        create_download_summary_file(session, str(summary_path))
        print(f"📋 Detailed report saved to: {summary_path}")

        # Download from specific channels only
        print(f"\n" + "=" * 50)
        print("🎯 Now downloading from specific channels...")

        # Get channel list first (you'd modify this with actual channel names)
        specific_channels = ["Channel1", "Channel2"]  # Replace with real names

        try:
            specific_session = await downloader.download_from_specific_channels(
                channel_names=specific_channels, mark_as_read=False
            )

            print(f"✅ Specific download completed:")
            print(f"   Files downloaded: {specific_session.total_downloaded}")

        except Exception as e:
            print(f"⚠️  Specific channel download failed: {e}")

        # Final statistics
        total_files = len(list(Path("advanced_downloads").rglob("*.*")))
        print(f"\n📊 Total files in download directory: {total_files}")


if __name__ == "__main__":
    asyncio.run(main())
