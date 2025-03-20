# pytest-sanitizer - Pytest Output Sanitizer for LLMs

A pytest plugin that sanitizes test output to prevent LLMs from seeing expected values in assertion errors.

## DISCLAIMER

**USE AT YOUR OWN RISK**: This tool is provided "AS IS" without any warranties or guarantees of any kind, express or implied. The author takes NO RESPONSIBILITY and accepts NO LIABILITY for any issues, failures, or damages that may arise from using this tool.

**NO WARRANTY**: There is absolutely no guarantee that this tool will work correctly or continue to work in the future. It may fail to sanitize certain outputs, miss assertion errors, or interfere with your test runs in unexpected ways.

**NO SUPPORT**: This is a personal tool not intended for production use. Issues, bugs, or compatibility problems will likely not be addressed.

If you use this tool and miss failing tests or if it causes any other problems in your testing process, that's entirely your responsibility.

## Maintenance Status

**Personal Tool**: This package is primarily developed for personal use and not actively maintained for the broader community. Feel free to use it, but be aware that issues and pull requests might not be addressed.

## Problem

LLMs sometimes "cheat" by looking at the expected values in assertion errors. For example, given an error like:

```
FAILED tests/test_utils.py::test_format_duration - AssertionError: assert '1d' == '1d 2h'
```

An LLM might modify the test to match the result given by the code, or worse, hardcode the expected result.

## Solution

pytest-sanitizer hooks into pytest's reporting system and sanitizes the output, removing the expected values from assertion errors while maintaining:
- Error tracebacks
- Colorized output
- Enough context to debug the issue

## Installation

For local installation from GitHub:

```bash
# Clone the repository
git clone https://github.com/username/pytest-sanitizer.git

# Install in development mode
cd pytest-sanitizer
pip install -e .
```

Or install from PyPI:

```bash
pip install pytest-sanitizer
```

## Usage

After installation, the plugin is automatically enabled when running pytest:

```bash
pytest tests/
```

The output will be sanitized to hide expected values in assertion errors.

You can also use the provided command-line tool:

```bash
pytest-sanitizer tests/
```

## Disabling Sanitization

For debugging or when you need to see the actual expected values, you can disable sanitization:

```bash
# Using pytest directly
pytest tests/ --no-sanitize  # or the shorter --ns flag

# Using the command-line tool
pytest-sanitizer tests/ --no-sanitize  # or --ns
```

## Example

Original pytest output:
```
FAILED tests/test_utils.py::test_format_duration - AssertionError: assert '1d' == '1d 2h'
```

Sanitized output:
```
FAILED tests/test_utils.py::test_format_duration - AssertionError: assert '1d' == [SANITIZED]

[NOTE: This output has been sanitized to prevent revealing expected values. You need to determine whether the issue is in the test or the implementation.]
```

## Demo

Run the included demo script to see how the sanitizer transforms assertion messages:

```bash
python demo.py
```

## License

MIT License 