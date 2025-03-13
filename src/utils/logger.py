import logging
import os
from typing import Dict, Any

DEFAULT_LOG_LEVEL = "INFO"

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(name: str) -> logging.Logger:
    """
    Create a configured logger instance
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    log_level_name = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    log_level = getattr(logging, log_level_name, logging.INFO)

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.setLevel(log_level)

        logger.propagate = False

    return logger
