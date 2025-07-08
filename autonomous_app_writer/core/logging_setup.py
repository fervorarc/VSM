"""
Sets up centralized logging for the agent.
"""

import logging
import sys
from autonomous_app_writer import config

def setup_logging():
    """
    Configures the root logger.
    """
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging configured.")

def get_logger(name):
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)
