"""
Centralized logging setup for the agent.
"""

import logging
import sys
from autonomous_app_writer import config

def setup_logging():
    """
    Configures the root logger for the application.
    """
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create handlers
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setFormatter(formatter)
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Add handlers to the root logger
    if not root_logger.handlers:
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)

def get_logger(name):
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)

# Setup logging on import
setup_logging()
