# Telegram Media Downloader

A modern, object-oriented Python application for downloading images and videos from unread messages in Telegram channels.

## ✨ Features

- 🔄 **Automatic Discovery**: Finds all your subscribed channels
- 📱 **Unread Only**: Processes only unread messages to avoid duplicates
- 🎯 **Smart Filtering**: Downloads only images and videos (customizable)
- 📁 **Organized Storage**: Creates separate folders for each channel
- 📄 **Metadata Preservation**: Saves message information alongside downloads
- ✅ **Read Marking**: Optionally marks messages as read after processing
- 🛠️ **Extensible Design**: Easy to customize with different filters and naming strategies
- 🔧 **Modern Python**: Built with async/await, type hints, and dataclasses
- 📊 **Detailed Reporting**: Comprehensive session summaries and statistics

## 🚀 Quick Start

### Installation with UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-media-downloader.git
cd telegram-media-downloader

# Install with UV
uv sync

# Install with development dependencies
uv sync --extra dev
```

### Configuration

Get Telegram API credentials:

1. Visit <https://my.telegram.org/apps>
2. Log in with your Telegram account
3. Create a new application
4. Note your api_id and api_hash

Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your credentials
```

Or export directly:

```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
export TELEGRAM_PHONE=+1234567890
# Optionally set the download directory
export TELEGRAM_DOWNLOAD_PATH=/path/to/downloads
```

### Usage

```bash
# Run the main application
make run
# or
uv run python -m telegram_media_downloader.main

# Specify a custom download directory
uv run python -m telegram_media_downloader.main --download-path /path/to/downloads

# Run with debug logging
make run-debug

# Run examples
make examples
```

## 🏗️ Architecture

The application follows SOLID principles with a clean, modular architecture:

```file
src/telegram_media_downloader/
├── config/          # Configuration management
├── models/          # Data models (MediaInfo, ChannelStats, etc.)
├── protocols/       # Interface definitions
├── filters/         # Media filtering strategies
├── namers/          # File naming strategies
├── core/            # Core functionality
├── utils/           # Utility functions
└── main.py          # Application entry point
```

**Key Components:**

- `TelegramConfig`: Configuration and validation
- `TelegramConnection`: Connection lifecycle management
- `ChannelManager`: Channel and message operations
- `MediaDownloader`: File download operations
- `TelegramMediaDownloader`: Main orchestrator

## 🎨 Customization

### Custom Media Filter

```python
from telegram_media_downloader import TelegramMediaDownloader, TelegramConfig

class VideoOnlyFilter:
    def should_download(self, message) -> bool:
        # Your custom logic here
        return is_video_message(message)

config = TelegramConfig.from_env()
async with TelegramMediaDownloader(
    config=config,
    media_filter=VideoOnlyFilter()
) as downloader:
    session = await downloader.download_all_unread_media()
```

### Custom File Naming

```python
class CustomFileNamer:
    def generate_filename(self, message, channel_name: str) -> str:
        return f"{channel_name}_{message.id}_{message.date.strftime('%Y%m%d')}"

# Use with downloader
downloader = TelegramMediaDownloader(
    config=config,
    file_namer=CustomFileNamer()
)
```

### Built-in Filters

- `DefaultMediaFilter`: Images and videos (default)
- `VideoOnlyFilter`: Videos only
- `ImageOnlyFilter`: Images only

### Built-in Namers

- `TimestampFileNamer`: YYYYMMDD_HHMMSS_msgID.ext (default)
- `ChannelPrefixNamer`: ChannelName_YYYYMMDD_HHMMSS_msgID.ext

## 📊 File Organization

```file
telegram_downloads/
├── Channel Name 1/
│   ├── 20240528_143022_msg123.jpg
│   ├── 20240528_143022_msg123.txt  # Message metadata
│   ├── 20240528_143045_msg124.mp4
│   └── 20240528_143045_msg124.txt
├── Channel Name 2/
│   └── ...
└── download_summary.txt  # Session summary
```

## 🧪 Development

```bash
# Install development dependencies
make dev

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Run all checks
make check

# Clean up
make clean
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_config/test_settings.py
```

## 📚 Examples

The `examples/` directory contains several usage examples:

- `basic_usage.py`: Simple download all media
- `custom_filter.py`: Custom filtering (large videos only)
- `custom_namer.py`: Custom file naming with organization
- `advanced_usage.py`: Advanced features demonstration

```bash
# Run specific example
make run-basic
make run-custom-filter
make run-advanced
```

## 🔧 Configuration Options

### Environment Variables

| Variable            | Description                        | Required | Default           |
|---------------------|------------------------------------|----------|-------------------|
| TELEGRAM_API_ID     | API ID from my.telegram.org        | Yes      | -                 |
| TELEGRAM_API_HASH   | API Hash from my.telegram.org      | Yes      | -                 |
| TELEGRAM_PHONE      | Phone number with country code     | Yes      | -                 |
| TELEGRAM_SESSION    | Session file name                  | No       | telegram_session  |
| LOG_LEVEL           | Logging level (DEBUG/INFO/...)     | No       | INFO              |

### Programmatic Configuration

```python
from telegram_media_downloader import TelegramConfig

# Direct configuration
config = TelegramConfig(
    api_id=12345,
    api_hash="your_hash",
    phone_number="+1234567890"
)

# From environment
config = TelegramConfig.from_env()

# Validation
errors = config.validate()
if errors:
    print("Configuration errors:", errors)
```

## 🚨 Error Handling

The application provides comprehensive error handling:

- **Connection errors**: Automatic retry and clear error messages
- **Download failures**: Individual file failures don't stop the session
- **Channel access issues**: Graceful handling of private/restricted channels
- **Rate limiting**: Automatic backoff and retry
- **Validation errors**: Clear configuration error messages

## 📈 Monitoring and Logging

- **Detailed logging**: Configurable log levels with colored output
- **Session summaries**: Comprehensive download statistics
- **Progress tracking**: Real-time download progress
- **Error reporting**: Detailed error logs and summaries
- **File reports**: Automatic generation of session reports

## 🔒 Security Considerations

- **Credential Management**: Use environment variables for API credentials
- **Session Files**: Keep .session files secure and private
- **Rate Limiting**: Built-in respect for Telegram's rate limits
- **Error Handling**: No sensitive data in error messages or logs

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and checks (`make check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

- **"Could not find the input entity"**:
  - Ensure you're subscribed to the channels
  - Check that channels are accessible

- **"Phone number invalid"**:
  - Include country code (e.g., +1 for US)
  - Ensure number is registered with Telegram

- **Authentication errors**:
  - Delete `.session` file and retry
  - Verify API credentials are correct

- **Permission denied**:
  - Some channels restrict downloading
  - Check channel settings and permissions

### Getting Help

- Check the Issues page
- Review the examples in the `examples/` directory
- Run with `LOG_LEVEL=DEBUG` for detailed logging

## 📞 Support

If you encounter issues:

- Check the troubleshooting section above
- Review existing GitHub issues
- Create a new issue with:
  - Description of the problem
  - Steps to reproduce
  - Error messages (with sensitive info removed)
  - Environment details (OS, Python version, etc.)
