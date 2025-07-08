"""
General utility functions for file operations.
"""

import os
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

def save_file(file_path, content):
    """
    Saves content to a file, creating directories if they don't exist.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"Successfully saved file to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving file to {file_path}: {e}")
        return False

def read_file(file_path):
    """
    Reads content from a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file from {file_path}: {e}")
        return None
