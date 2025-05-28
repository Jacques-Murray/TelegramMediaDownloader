# Complete Setup Commands

## 🚀 Quick Setup

```bash
# 1. Create project directory
mkdir telegram-media-downloader
cd telegram-media-downloader

# 2. Initialize UV project
uv init .

# 3. Create directory structure
mkdir -p src/telegram_media_downloader/{config,models,protocols,filters,namers,core,utils}
mkdir -p tests/{test_config,test_models,test_filters,test_namers,test_core}
mkdir -p examples
mkdir -p docs

# 4. Install dependencies
uv add telethon
uv add --dev pytest pytest-asyncio pytest-cov black isort flake8 mypy pre-commit

# 5. Copy all the source files (use the artifacts provided above)

# 6. Set up environment
cp .env.example .env
# Edit .env with your Telegram credentials

# 7. Install in development mode
uv sync --extra dev

# 8. Run the application
uv run python -m telegram_media_downloader.main
```

## 📁 Complete File Structure

Here's the complete project structure you should have:

```file
telegram-media-downloader/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── Makefile
├── .pre-commit-config.yaml
├── LICENSE
├── src/
│   └── telegram_media_downloader/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── media_info.py
│       │   ├── channel_stats.py
│       │   └── download_session.py
│       ├── protocols/
│       │   ├── __init__.py
│       │   ├── media_filter.py
│       │   └── file_namer.py
│       ├── filters/
│       │   ├── __init__.py
│       │   ├── default_filter.py
│       │   ├── video_filter.py
│       │   └── image_filter.py
│       ├── namers/
│       │   ├── __init__.py
│       │   ├── timestamp_namer.py
│       │   └── channel_prefix_namer.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   ├── channel_manager.py
│       │   ├── media_downloader.py
│       │   └── downloader.py
│       └── utils/
│           ├── __init__.py
│           ├── logging.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config/
│   │   ├── __init__.py
│   │   └── test_settings.py
│   ├── test_models/
│   │   ├── __init__.py
│   │   ├── test_media_info.py
│   │   └── test_channel_stats.py
│   ├── test_filters/
│   │   ├── __init__.py
│   │   └── test_default_filter.py
│   ├── test_namers/
│   │   ├── __init__.py
│   │   └── test_timestamp_namer.py
│   └── test_core/
│       ├── __init__.py
│       ├── test_connection.py
│       └── test_downloader.py
├── examples/
│   ├── __init__.py
│   ├── basic_usage.py
│   ├── custom_filter.py
│   ├── custom_namer.py
│   └── advanced_usage.py
└── docs/
    ├── api.md
    ├── configuration.md
    └── examples.md
```

## 🔧 Development Workflow

```bash
# 1. Set up development environment
make dev

# 2. Configure pre-commit hooks
uv run pre-commit install

# 3. Run tests to verify setup
make test

# 4. Format and lint code
make check

# 5. Run the application
make run
```

## ⚙️ Environment Setup

Create your `.env` file:

```bash
# Copy example
cp .env.example .env

# Edit with your credentials
nano .env  # or your preferred editor
```

Your `.env` should look like:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_from_telegram
TELEGRAM_PHONE=+1234567890
TELEGRAM_SESSION=telegram_session
LOG_LEVEL=INFO
```

## 🧪 Testing the Setup

```bash
# 1. Test configuration
uv run python -c "
from src.telegram_media_downloader.config.settings import TelegramConfig
config = TelegramConfig.from_env()
errors = config.validate()
if errors:
    print('Configuration errors:', errors)
else:
    print('✅ Configuration is valid!')
"

# 2. Test imports
uv run python -c "
from src.telegram_media_downloader import TelegramMediaDownloader, TelegramConfig
print('✅ All imports working!')
"

# 3. Run basic test
make test

# 4. Run the application (will connect to Telegram)
make run
```

## 📦 Building and Distribution

```bash
# Build the package
make build

# This creates:
# - dist/telegram_media_downloader-1.0.0-py3-none-any.whl
# - dist/telegram_media_downloader-1.0.0.tar.gz

# Install from built package
uv pip install dist/telegram_media_downloader-1.0.0-py3-none-any.whl
```

## 🚨 Important Notes

1. **API Credentials**: Never commit your `.env` file or API credentials to version control.

2. **Session Files**: The `.session` files contain authentication data. Keep them secure and don't share them.

3. **Rate Limits**: Telegram has rate limits. The application handles this automatically, but be mindful when downloading large amounts of media.

4. **Legal Compliance**: Respect copyright and terms of service. Only download content you have permission to download.

5. **Privacy**: Be mindful of the channels' rules and Telegram's terms of service.

## 🎯 Usage Examples

Once set up, you can use the application in various ways:

```bash
# Basic usage - download all unread media
make run

# Download with debug logging
make run-debug

# Run specific examples
make run-basic           # Basic usage example
make run-custom-filter   # Custom filter example
make run-custom-namer    # Custom naming example
make run-advanced        # Advanced features example
```

## 🔍 Verification Checklist

Before using the application, verify:

- [ ] All files are in the correct directory structure
- [ ] Dependencies are installed (`uv sync` completed successfully)
- [ ] Environment variables are set in `.env`
- [ ] Configuration validates without errors
- [ ] Tests pass (`make test`)
- [ ] Application starts without import errors

## 🆘 Common Setup Issues

**Import Errors:**

```bash
# Make sure you're using the correct Python path
uv run python -m telegram_media_downloader.main
# Not: python -m telegram_media_downloader.main
```

**Missing Dependencies:**

```bash
# Reinstall dependencies
uv sync --reinstall
```

**Configuration Issues:**

```bash
# Check your .env file exists and has correct values
cat .env
# Verify configuration
uv run python -c "from src.telegram_media_downloader.config.settings import TelegramConfig; print(TelegramConfig.from_env().validate())"
``
