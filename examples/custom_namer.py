"""Custom file naming example."""

import asyncio
from pathlib import Path
from telegram_media_downloader import (
    TelegramMediaDownloader, 
    TelegramConfig,
    TimestampFileNamer
)
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class OrganizedFileNamer:
    """File namer that organizes files by type and date."""
    
    def generate_filename(self, message, channel_name: str) -> str:
        """Generate organized filename."""
        # Get file type
        file_type = self._get_file_type(message)
        
        # Get date parts
        date = message.date
        year_month = date.strftime("%Y-%m")
        
        # Sanitize channel name
        safe_channel = self._sanitize_name(channel_name)
        
        # Generate filename
        timestamp = date.strftime("%d_%H%M%S")
        extension = self._get_extension(message)
        
        return f"{file_type}/{year_month}/{safe_channel}_{timestamp}_msg{message.id}{extension}"
    
    def _get_file_type(self, message) -> str:
        """Determine file type folder."""
        if isinstance(message.media, MessageMediaPhoto):
            return "images"
        elif isinstance(message.media, MessageMediaDocument):
            doc = message.media.document
            if doc.mime_type:
                if doc.mime_type.startswith('video/'):
                    return "videos"
                elif doc.mime_type.startswith('image/'):
                    return "images"
                elif doc.mime_type.startswith('audio/'):
                    return "audio"
            return "documents"
        return "other"
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for filename."""
        return "".join(c for c in name if c.isalnum() or c in '-_')[:30]
    
    def _get_extension(self, message) -> str:
        """Get file extension."""
        if isinstance(message.media, MessageMediaPhoto):
            return '.jpg'
        elif isinstance(message.media, MessageMediaDocument):
            doc = message.media.document
            if doc.mime_type:
                return '.' + doc.mime_type.split('/')[-1]
        return '.bin'


async def main():
    """Organized file naming example."""
    print("📁 Organized File Naming Example")
    
    config = TelegramConfig.from_env()
    
    if config.validate():
        print("Please configure your Telegram credentials.")
        return
    
    async with TelegramMediaDownloader(
        config=config,
        file_namer=OrganizedFileNamer(),
        download_path='organized_downloads'
    ) as downloader:
        
        print("📋 Downloading with organized file structure...")
        session = await downloader.download_all_unread_media()
        
        print(f"✅ Organized {session.total_downloaded} files by type and date")
        
        # Show directory structure
        base_path = Path('organized_downloads')
        if base_path.exists():
            print(f"\n📂 Directory structure:")
            for item in sorted(base_path.rglob('*/')):
                level = len(item.relative_to(base_path).parts)
                indent = "  " * level
                print(f"{indent}{item.name}/")


if __name__ == '__main__':
    asyncio.run(main())