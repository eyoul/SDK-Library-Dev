"""
Safaricom M-PESA SDK
A Python SDK for integrating with Safaricom M-PESA APIs
"""

# Importing necessary components
from .test_client import TestMPESAClient  # Client for M-PESA API interactions
from .test_config import TestConfiguration  # Configuration settings for the SDK
from .test_auth import TestAuthentication  # Authentication methods for API access

# Versioning information
__version__ = "1.0.0"

# Public API surface
__all__ = ["TestMPESAClient", "TestConfiguration", "TestAuthentication"]