"""Main entry point for the Telegram Media Downloader."""

import asyncio
import sys
from pathlib import Path

from .config.settings import TelegramConfig
from .core.downloader import TelegramMediaDownloader
from .utils.logging import setup_colored_logging
from .utils.helpers import print_session_summary, create_download_summary_file


async def main() -> None:
    """Main application entry point."""
    # Setup logging
    setup_colored_logging('INFO')
    
    print("🚀 Telegram Media Downloader")
    print("=" * 50)
    
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
            print("   - TELEGRAM_API_ID (your API ID from https://my.telegram.org/apps)")
            print("   - TELEGRAM_API_HASH (your API hash from https://my.telegram.org/apps)")
            print("   - TELEGRAM_PHONE (your phone number with country code)")
            print("\n💡 You can also create a .env file with these variables.")
            
            sys.exit(1)
        
        print(f"📱 Connecting with phone: {config.phone_number}")
        print(f"📁 Downloads will be saved to: {Path('telegram_downloads').absolute()}")
        
        # Initialize and run downloader
        async with TelegramMediaDownloader(
            config=config,
            download_path='telegram_downloads'
        ) as downloader:
            
            print("\n🔍 Scanning channels for unread media...")
            session = await downloader.download_all_unread_media(mark_as_read=True)
            
            # Print summary
            print_session_summary(session)
            
            # Save summary to file
            summary_file = Path('telegram_downloads') / 'download_summary.txt'
            create_download_summary_file(session, str(summary_file))
            print(f"\n📋 Session summary saved to: {summary_file}")
            
            # Final status
            if session.total_downloaded > 0:
                print(f"\n✅ Successfully downloaded {session.total_downloaded} files!")
            else:
                print(f"\n ℹ️  No new media files found to download.")
                
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


if __name__ == '__main__':
    cli_main()