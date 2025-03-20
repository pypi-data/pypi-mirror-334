"""
Logging configuration for the Ocular SDK.
"""

import logging
import sys
import os
from typing import Optional, Union, TextIO

# Add this flag to track if setup has been done
_LOGGING_INITIALIZED = False


def setup_logging(
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
    stream: Optional[TextIO] = sys.stdout,
    name: str = "ocular",
) -> logging.Logger:
    """
    Set up logging for the Ocular SDK.

    Args:
        level (Union[int, str], optional): Logging level. Defaults to logging.INFO.
        format_string (str, optional): Log format string. Defaults to None.
        log_file (str, optional): Path to log file. Defaults to None.
        stream (TextIO, optional): Stream to log to. Defaults to sys.stdout.
        name (str, optional): Logger name. Defaults to "ocular".

    Returns:
        logging.Logger: Configured logger
    """
    global _LOGGING_INITIALIZED

    logger = logging.getLogger(name)

    # Only set up logging once per name
    if _LOGGING_INITIALIZED:
        return logger

    # Set log level from environment variable if defined
    env_level = os.environ.get("OCULAR_LOG_LEVEL", "").upper()
    if env_level:
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        level = level_map.get(env_level, level)

    logger.setLevel(level)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Default format string if not provided
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)

    # Stream handler (console)
    if stream:
        stream_handler = logging.StreamHandler(stream)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # File handler (if log_file is provided)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    # Mark as initialized
    _LOGGING_INITIALIZED = True

    return logger


def get_logger(name: str = "ocular") -> logging.Logger:
    """
    Get the Ocular logger. If this is the first time getting this logger,
    set it up with default configuration.

    Args:
        name (str, optional): Logger name. Defaults to "ocular".

    Returns:
        logging.Logger: The logger
    """
    logger = logging.getLogger(name)

    # If the logger doesn't have handlers yet, set it up with defaults
    if not logger.handlers:
        return setup_logging(name=name)

    return logger
