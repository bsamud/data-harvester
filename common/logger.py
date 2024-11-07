"""Logging utilities for dataHarvest"""
import logging
import sys
from datetime import datetime

def get_logger(name, log_file=None, level=logging.INFO):
    """
    Create a logger with console and optional file output

    Args:
        name: Logger name
        log_file: Optional log file path
        level: Logging level

    Returns:
        logging.Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Default logger
log = get_logger('dataHarvest')
