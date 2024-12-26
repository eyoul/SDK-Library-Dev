"""
Safaricom M-PESA SDK
A Python SDK for integrating with Safaricom M-PESA APIs
"""

from .client import MPESAClient
from .config import Configuration
from .auth import Authentication
from .exceptions import MPESAError

__version__ = "1.0.0"
__all__ = ["MPESAClient", "Configuration", "Authentication", "MPESAError"]
