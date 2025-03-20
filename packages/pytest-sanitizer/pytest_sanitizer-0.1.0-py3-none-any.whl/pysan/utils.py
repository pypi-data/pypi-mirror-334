"""
Utility functions for pysan.
"""
import os
import sys
from typing import List, Optional


def is_colorized_output_enabled() -> bool:
    """
    Check if colorized output is enabled.
    
    Returns:
        bool: True if colorized output is enabled
    """
    # Check for NO_COLOR environment variable (https://no-color.org/)
    if os.environ.get("NO_COLOR") is not None:
        return False
    
    # Check if output is a terminal
    if not sys.stdout.isatty():
        return False
    
    # Check if TERM is set to dumb
    if os.environ.get("TERM") == "dumb":
        return False
    
    # Check for --color=no or --no-color in command line args
    for arg in sys.argv:
        if arg in ("--no-color", "--color=no"):
            return False
    
    return True


def format_sanitized_message(original: str) -> str:
    """
    Format a sanitized message with a warning.
    
    Args:
        original: The original sanitized message
        
    Returns:
        The formatted message with a warning about sanitization
    """
    warning = "\n[NOTE: This output has been sanitized to prevent revealing expected values. " \
              "You need to determine whether the issue is in the test or the implementation.]"
    
    return original + warning 