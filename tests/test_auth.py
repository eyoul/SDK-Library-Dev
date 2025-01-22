# test_auth.py
import unittest
import requests  
from unittest.mock import patch, MagicMock
from safaricom_sdk.auth import Authentication
from safaricom_sdk.config import Configuration
from safaricom_sdk.exceptions import MPESAError

class TestAuthentication(unittest.TestCase):

    @patch('safaricom_sdk.auth.requests.get')
    def test_get_access_token(self, mock_get):
        # Setup
        config = Configuration(consumer_key='test_key', consumer_secret='test_secret', timeout=5)
        auth = Authentication(config)
        
        # Mock the response for the access token
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = {
            "access_token": "mock_access_token",
            "expires_in": "3600"
        }
        
        # Act
        token = auth.get_access_token()
        
        # Assert
        self.assertEqual(token, "mock_access_token")
        self.assertIsNotNone(auth._token_expiry)

    @patch('safaricom_sdk.auth.requests.get')
    def test_refresh_access_token_failure(self, mock_get):
        # Setup
        config = Configuration(consumer_key='test_key', consumer_secret='test_secret', timeout=5)
        auth = Authentication(config)
        
        # Mock a failed request
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        # Act & Assert
        with self.assertRaises(MPESAError):
            auth._refresh_access_token()

if __name__ == '__main__':
    unittest.main()