"""Main entry point for the Telegram Media Downloader."""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from .config.settings import TelegramConfig
from .core.downloader import TelegramMediaDownloader
from .utils.helpers import create_download_summary_file, print_session_summary
from .utils.logging import setup_colored_logging


async def main() -> None:
    """Main application entry point."""
    # Setup logging
    setup_colored_logging("INFO")

    print("🚀 Telegram Media Downloader")
    print("=" * 50)

    parser = argparse.ArgumentParser(description="Telegram Media Downloader")
    parser.add_argument(
        "--download-path",
        type=str,
        default=os.getenv("TELEGRAM_DOWNLOAD_PATH", "telegram_downloads"),
        help=(
            "Directory to save downloaded media. "
            "Default: telegram_downloads or $TELEGRAM_DOWNLOAD_PATH."
        ),
    )
    args, _ = parser.parse_known_args()
    download_path = args.download_path

    try:
        # Load configuration from environment
        config = TelegramConfig.from_env()

        # Validate configuration
        errors = config.validate()
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")

            print("\n💡 Please set the following environment variables:")
            print(
                "   - TELEGRAM_API_ID (your API ID from https://my.telegram.org/apps)"
            )
            print(
                "   - TELEGRAM_API_HASH (your API hash from https://my.telegram.org/apps)"
            )
            print("   - TELEGRAM_PHONE (your phone number with country code)")
            print("\n💡 You can also create a .env file with these variables.")

            sys.exit(1)

        print("📱 Connecting with phone:")
        print(config.phone_number)
        print("📁 Downloads will be saved to:")
        print(Path(download_path).absolute())

        # Initialize and run downloader
        async with TelegramMediaDownloader(
            config=config, download_path=download_path
        ) as downloader:

            print("\n🔍 Scanning channels for unread media...")
            session = await downloader.download_all_unread_media(mark_as_read=True)

            # Print summary
            print_session_summary(session)

            # Save summary to file
            summary_file = Path(download_path) / "download_summary.txt"
            create_download_summary_file(session, str(summary_file))
            print("\n📋 Session summary saved to:")
            print(summary_file)

            # Final status
            if session.total_downloaded > 0:
                print(
                    f"\n✅ Successfully downloaded "
                    f"{session.total_downloaded} files!"
                )
            else:
                print("\n ℹ️  No new media files found to download.")

    except KeyboardInterrupt:
        print("\n\n⏹️  Download interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Application error: {e}")
        sys.exit(1)


def cli_main() -> None:
    """CLI entry point wrapper."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    cli_main()
