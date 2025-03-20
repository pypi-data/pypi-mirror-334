# internal-link-juicer-api/__init__.py
"""
Internal Link Juicer API Client

This package provides a Python client for interacting with the
Internal Link Juicer WordPress plugin's REST API. It allows you to
retrieve and update link definitions programmatically.

Version: 1
Author: Onur Gürpınar
"""

__version__ = "0.1.0"  # Keep this in sync with setup.py
__author__ = "Onur Gürpınar"
__description__ = "A Python client for the Internal Link Juicer WordPress plugin API."

# Import the main class so it's available directly from the package.
from .ilj_api_client import ILJDefinitionAPIClient

# Make ILJDefinitionAPIClient available when importing the package directly
__all__ = ["ILJDefinitionAPIClient"]
__version__ = "1.0.3"
