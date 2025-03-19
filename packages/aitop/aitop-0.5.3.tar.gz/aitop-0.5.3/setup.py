#!/usr/bin/env python3
"""Setup script for AITop."""
from setuptools import setup, find_packages
from pathlib import Path

# Get version from version.py
exec(open('aitop/version.py').read())

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aitop",
    version=__version__,
    description="A system monitor focused on AI/ML workload monitoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alexander Warth",
    author_email="alexander.warth@mailbox.org",
    url="https://gitlab.com/CochainComplex/aitop",
    project_urls={
        "Homepage": "https://gitlab.com/CochainComplex/aitop",
        "Source": "https://gitlab.com/CochainComplex/aitop",
        "Bug Tracker": "https://gitlab.com/CochainComplex/aitop/-/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0,<6.0.0",  # System monitoring (CPU, memory, processes)
        "click>=8.1.0,<9.0.0",   # Command line interface
    ],
    extras_require={
        "dev": [
            "black>=23.0.0,<24.0.0",
            "mypy>=1.0.0,<2.0.0",
            "pytest>=7.0.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "pylint>=2.17.0,<3.0.0",
            "isort>=5.12.0,<6.0.0",
            "flake8>=6.1.0,<7.0.0",
            "pre-commit>=3.3.0,<4.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0,<8.0.0",
            "sphinx-rtd-theme>=1.3.0,<2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aitop=aitop.__main__:main",
        ],
    },
    package_data={
        "aitop": ["config/*.json"],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
    ],
)
