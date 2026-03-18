"""Simple logging configuration for the application."""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Global flag to ensure we only configure once
_logging_configured = False

# Log file prefix -- rename for your project (e.g. "shh-app", "mtus-app")
_LOG_FILE_PREFIX = "my-app"


def configure_root_logging() -> None:
    """
    Configure root logging for the entire application with file and console output.

    Logs are written to:
    - Console (stdout) for real-time monitoring
    - logs/{_LOG_FILE_PREFIX}-YYYY-MM-DD.log with daily rotation
    """
    global _logging_configured

    if _logging_configured:
        return

    log_level = get_log_level()

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Setup formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with daily rotation
    log_filename = log_dir / f"{_LOG_FILE_PREFIX}-{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = TimedRotatingFileHandler(
        filename=str(log_filename),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    def rotation_namer(default_name):
        parts = default_name.split('.')
        if len(parts) >= 3:
            date_str = parts[-1]
            return f"{log_dir}/{_LOG_FILE_PREFIX}-{date_str}.log"
        return default_name

    file_handler.namer = rotation_namer
    root_logger.addHandler(file_handler)

    _logging_configured = True


def get_log_level() -> int:
    """Get the log level from environment variable."""
    log_level_str = os.getenv("APP_LOG_LEVEL", "INFO").upper()

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    return level_map.get(log_level_str, logging.INFO)


def setup_logger(name: str, level: int | None = None) -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger(name)

    if level is None:
        level = get_log_level()

    logger.setLevel(level)
    logger.propagate = True

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger by name."""
    return setup_logger(name)
