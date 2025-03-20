"""
Setup script for pytest-sanitizer package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-sanitizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A pytest plugin to sanitize output for LLMs (personal tool, no warranty or liability)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pytest-sanitizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Framework :: Pytest",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=6.0.0",
    ],
    entry_points={
        "pytest11": [
            "sanitizer = pytest_sanitizer.plugin",
        ],
        "console_scripts": [
            "pytest-sanitizer=pytest_sanitizer.cli:main",
        ],
    },
) 