# test_auth.py
import unittest
import requests  
from unittest.mock import patch, MagicMock
from safaricom_sdk.auth import Authentication
from safaricom_sdk.config import Configuration
from safaricom_sdk.exceptions import MPESAError

class TestAuthentication(unittest.TestCase):

    @patch('safaricom_sdk.auth.requests.request')
    def test_get_access_token(self, mock_request):
        # Setup
        config = Configuration(consumer_key='test_key', consumer_secret='test_secret', timeout=5)
        auth = Authentication(config)
        
        # Mock the response for the access token
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "mock_access_token", "expires_in": 3600}'
        mock_request.return_value = mock_response
        
        # Act
        token = auth.get_access_token()
        
        # Assert
        self.assertEqual(token, "mock_access_token")
        self.assertIsNotNone(auth._token_expiry)
        
        # Verify the request was made with correct headers
        mock_request.assert_called_once_with(
            method='GET', 
            url='https://apisandbox.safaricom.et/v1/token/generate?grant_type=client_credentials', 
            headers={'Authorization': 'Basic dGVzdF9rZXk6dGVzdF9zZWNyZXQ='}, 
            verify=True,
            timeout=15
        )

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