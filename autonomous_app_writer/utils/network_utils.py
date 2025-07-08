"""
General utility functions for network operations.
"""

import requests
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

def fetch_url_content(url, timeout=10):
    """
    Fetches the content from a given URL.

    Args:
        url (str): The URL to fetch.
        timeout (int): The request timeout in seconds.

    Returns:
        str: The content of the page, or None if an error occurs.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None
