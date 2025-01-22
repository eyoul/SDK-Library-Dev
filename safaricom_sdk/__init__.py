"""
Safaricom M-PESA SDK
A Python SDK for integrating with Safaricom M-PESA APIs
"""

# Importing necessary components
from .client import MPESAClient  # Client for M-PESA API interactions
from .config import Configuration  # Configuration settings for the SDK
from .auth import Authentication  # Authentication methods for API access
from .exceptions import MPESAError  # Custom exceptions for error handling

# Versioning information
__version__ = "1.0.0"

# Public API surface
__all__ = ["MPESAClient", "Configuration", "Authentication", "MPESAError"]