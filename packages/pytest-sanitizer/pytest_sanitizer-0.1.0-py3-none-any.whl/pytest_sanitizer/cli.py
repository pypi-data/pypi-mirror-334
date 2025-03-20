"""
Command-line interface for running pytest with sanitization.
"""
import sys
import pytest
import argparse


def main():
    """
    Main entry point for the pytest-sanitizer command-line tool.
    Passes all arguments to pytest while ensuring the sanitizer plugin is loaded.
    
    Use --no-sanitize or --ns to disable sanitization (for debugging purposes).
    """
    # Parse our own args first to check for help
    parser = argparse.ArgumentParser(
        description="Run pytest with output sanitization for LLMs",
        add_help=False  # Don't add help, just handle it ourselves first
    )
    parser.add_argument(
        "--help", "-h", 
        action="store_true", 
        help="Show this help message and exit"
    )
    parser.add_argument(
        "--no-sanitize", "--ns",
        action="store_true",
        help="Disable output sanitization (for debugging)"
    )
    
    # Only parse known args, letting pytest handle the rest
    args, remaining = parser.parse_known_args()
    
    if args.help:
        parser.print_help()
        print("\nAll other pytest arguments are supported. See 'pytest --help' for more options.")
        sys.exit(0)
    
    # Prepare arguments for pytest
    pytest_args = remaining
    
    # Pass the flag to pytest if specified (using either --no-sanitize or --ns)
    if args.no_sanitize:
        if "--no-sanitize" not in pytest_args and "--ns" not in pytest_args:
            pytest_args.append("--no-sanitize")
    
    # Run pytest with our args
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main()) 