"""
Pytest plugin for sanitizing test output to prevent LLMs from seeing expected values.
"""
import re
import pytest
from _pytest.config import Config
from _pytest.terminal import TerminalReporter
from pysan.sanitizer import sanitize_message
from pysan.utils import format_sanitized_message


class SanitizedTerminalReporter(TerminalReporter):
    """Custom terminal reporter that sanitizes assertion errors."""
    
    def _report_testfailed(self, rep):
        """Override the test failure reporting method to sanitize output."""
        sanitized = sanitize_message(rep)
        
        # If sanitization modified the message, add a note
        if sanitized:
            rep.longrepr = format_sanitized_message(sanitized)
        
        # Call the original implementation with sanitized report
        super()._report_testfailed(rep)


def pytest_configure(config: Config):
    """Hook to configure pytest with our custom terminal reporter."""
    # Replace the default terminal reporter with our sanitized version
    original_reporter = config.pluginmanager.getplugin("terminalreporter")
    if original_reporter:
        config.pluginmanager.unregister(original_reporter)
        sanitized_reporter = SanitizedTerminalReporter(config)
        config.pluginmanager.register(sanitized_reporter, "terminalreporter") 