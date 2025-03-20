"""
Pytest plugin for sanitizing test output to prevent LLMs from seeing expected values.
"""
import sys
import pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from pytest_sanitizer.sanitizer import sanitize_message
from pytest_sanitizer.utils import format_sanitized_message


def pytest_addoption(parser):
    """
    Add command-line options to pytest.
    """
    group = parser.getgroup("sanitizer")
    group.addoption(
        "--no-sanitize", "--ns",
        action="store_true", 
        default=False,
        help="Disable output sanitization"
    )


# Store config for later use
_config = None


def pytest_configure(config: Config):
    """
    Hook to configure pytest.
    
    This is called when pytest is starting up, before collecting tests.
    """
    global _config
    _config = config


@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report: TestReport):
    """
    Hook that intercepts test reports before they're displayed.
    
    This hook is called for every test report, including setup, call, and teardown phases.
    We only want to sanitize the failure reports during the call phase.
    """
    # Skip sanitization if the --no-sanitize flag is used
    global _config
    if _config and _config.option.no_sanitize:
        return

    if report.when == "call" and report.failed:
        sanitized = sanitize_message(report)
        if sanitized:
            report.longrepr = format_sanitized_message(sanitized) 