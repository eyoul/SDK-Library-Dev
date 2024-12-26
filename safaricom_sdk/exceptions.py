class MPESAError(Exception):
    """Base exception for M-PESA SDK"""
    pass

class ConfigurationError(MPESAError):
    """Raised when there's a configuration error"""
    pass

class AuthenticationError(MPESAError):
    """Raised when authentication fails"""
    pass

class APIError(MPESAError):
    """Raised when an API request fails"""
    def __init__(self, message: str, response_code: str = None, response_description: str = None):
        self.response_code = response_code
        self.response_description = response_description
        super().__init__(message)

class ValidationError(MPESAError):
    """Raised when request validation fails"""
    pass
