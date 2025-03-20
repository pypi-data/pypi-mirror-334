import os
from setuptools import setup, find_packages
from typing import List, Optional
from importlib.metadata import version as get_version

def read_requirements(file_path: str) -> List[str]:
    """Reads requirements from a file and returns them as a list.

    Args:
        file_path (str): Path to the requirements file.

    Returns:
        List[str]: List of dependency strings.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def read_description(file_path: str) -> str:
    """Reads the long description from a file.

    Args:
        file_path (str): Path to the description file (e.g., README.md).

    Returns:
        str: The long description content.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
try:
    from neongram import __version__ as version
except ImportError:
    version = "0.1.0"  

setup(
    name="neongram",
    version=version,
    description="A modern MTProto-based Telegram client library",
    long_description=read_description("README.md"),
    long_description_content_type="text/markdown",
    author="SANTHOSH",
    author_email="telegramsanthu@gmail.com",
    url="https://github.com/bcncalling/neongram",
    packages=find_packages(where="neongram"),
    package_dir={"": "neongram"},
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt")
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
    ],
    keywords="telegram mtproto client api",
    license="GNU General Public License v3 (GPLv3)",
    include_package_data=True,
    zip_safe=False,
)