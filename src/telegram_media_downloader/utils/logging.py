"""Logging configuration utilities."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: str = 'INFO',
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        include_timestamp: Whether to include timestamp in log messages
    """
    # Default format string
    if format_string is None:
        if include_timestamp:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else:
            format_string = '%(name)s - %(levelname)s - %(message)s'
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )
    
    # Set specific loggers to appropriate levels
    # Reduce noise from telethon
    logging.getLogger('telethon').setLevel(logging.WARNING)
    
    # Create application logger
    logger = logging.getLogger('telegram_media_downloader')
    logger.info(f"Logging configured at {level} level")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'telegram_media_downloader.{name}')


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for better readability."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Add color to level name
        level_color = self.COLORS.get(record.levelname, '')
        if level_color:
            record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        
        return super().format(record)


def setup_colored_logging(level: str = 'INFO') -> None:
    """
    Setup colored logging for better console output.
    
    Args:
        level: Logging level
    """
    # Create colored formatter
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.handlers.clear()  # Remove existing handlers
    root_logger.addHandler(console_handler)
    
    # Reduce telethon noise
    logging.getLogger('telethon').setLevel(logging.WARNING)