#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Pyqtfork.

This script handles the packaging and distribution of Pyqtfork for PyPI.
"""

import os
import sys
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Version of Pyqtfork
version = '1.0.0'

setup(
    name="Pyqtfork",
    version=version,
    description="Pyqtfork - Enhanced Python bindings for Qt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pyqtfork Contributors",
    author_email="info@pyqtfork.org",
    url="https://github.com/pyqtfork/pyqtfork",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "PyQt5>=5.10.1",  # Pyqtfork is built on top of PyQt5
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="qt gui pyqt pyqtfork ui interface fork",
    project_urls={
        "Documentation": "https://pyqtfork.readthedocs.io/",
        "Source": "https://github.com/pyqtfork/pyqtfork",
        "Tracker": "https://github.com/pyqtfork/pyqtfork/issues",
    },
)#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for PYUI.

This script handles the packaging and distribution of PYUI for PyPI.
"""

import os
import sys
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Version of PYUI
version = '1.0.0'

setup(
    name="pyui",
    version=version,
    description="PYUI - Enhanced Python bindings for Qt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PYUI Contributors",
    author_email="info@pyui.org",
    url="https://github.com/pyui/pyui",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "PyQt5>=5.10.1",  # PYUI is built on top of PyQt5
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="qt gui pyqt pyui ui interface",
    project_urls={
        "Documentation": "https://pyui.readthedocs.io/",
        "Source": "https://github.com/pyui/pyui",
        "Tracker": "https://github.com/pyui/pyui/issues",
    },
)