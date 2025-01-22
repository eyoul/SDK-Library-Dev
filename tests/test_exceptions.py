# tests/test_exceptions.py
import unittest
from safaricom_sdk.exceptions import (
    MPESAError, 
    ConfigurationError, 
    AuthenticationError, 
    APIError, 
    ValidationError
)

class TestExceptions(unittest.TestCase):
    def test_mpesa_base_error(self):
        # Test base MPESAError
        with self.assertRaises(MPESAError):
            raise MPESAError("Generic MPESA error")

    def test_configuration_error(self):
        # Test ConfigurationError
        with self.assertRaises(ConfigurationError):
            raise ConfigurationError("Configuration is invalid")
        
        # Verify it's a subclass of MPESAError
        self.assertTrue(issubclass(ConfigurationError, MPESAError))

    def test_authentication_error(self):
        # Test AuthenticationError
        with self.assertRaises(AuthenticationError):
            raise AuthenticationError("Authentication failed")
        
        # Verify it's a subclass of MPESAError
        self.assertTrue(issubclass(AuthenticationError, MPESAError))

    def test_api_error(self):
        # Test APIError with full details
        error = APIError(
            message="API request failed", 
            response_code="500", 
            response_description="Internal Server Error"
        )
        
        # Check error attributes
        self.assertEqual(error.response_code, "500")
        self.assertEqual(error.response_description, "Internal Server Error")
        self.assertTrue("API request failed" in str(error))
        
        # Verify it's a subclass of MPESAError
        self.assertTrue(issubclass(APIError, MPESAError))

    def test_validation_error(self):
        # Test ValidationError
        with self.assertRaises(ValidationError):
            raise ValidationError("Validation failed")
        
        # Verify it's a subclass of MPESAError
        self.assertTrue(issubclass(ValidationError, MPESAError))

    def test_exception_hierarchy(self):
        # Verify all custom exceptions inherit from MPESAError
        custom_exceptions = [
            ConfigurationError, 
            AuthenticationError, 
            APIError, 
            ValidationError
        ]
        
        for exc in custom_exceptions:
            self.assertTrue(issubclass(exc, MPESAError), 
                            f"{exc.__name__} should inherit from MPESAError")

if __name__ == '__main__':
    unittest.main()
