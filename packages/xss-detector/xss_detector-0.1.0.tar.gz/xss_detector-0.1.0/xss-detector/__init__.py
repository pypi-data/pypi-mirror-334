"""
XSS Detector - A Python package for detecting Cross-Site Scripting (XSS) attacks.
"""

__version__ = '0.1.0'

from .detector import XSSDetector
from .api import create_app

__all__ = ['XSSDetector', 'create_app']