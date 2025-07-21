#!/usr/bin/env python3
"""
Setup script for Browser Scraper
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
install_requires = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="browser-scraper",
    version="2.0.0",
    author="Browser Scraper Team",
    description="A comprehensive web scraping tool with GUI and CLI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "browser-scraper=src.main:main",
            "scraper-gui=src.ui.gui_simple:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="web scraping selenium browser automation gui cli",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/browser-scraper/issues",
        "Source": "https://github.com/your-repo/browser-scraper",
        "Documentation": "https://github.com/your-repo/browser-scraper#readme",
    },
) 