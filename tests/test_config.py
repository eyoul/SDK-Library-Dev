import unittest
from unittest.mock import patch, MagicMock
from safaricom_sdk.config import Configuration

class TestConfiguration(unittest.TestCase):
    
    @patch('safaricom_sdk.config.requests.request')
    def test_get_access_token(self, mock_request):
        # Mock the response
        mock_response = {
            "access_token": "mock_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_request.return_value = MagicMock(status_code=200, json=lambda: mock_response)

        config = Configuration()  # Create an instance of Configuration
        token = config.get_access_token()  # Call the method to get the access token
        self.assertEqual(token['access_token'], "mock_access_token")
        print("Mocked access token retrieved successfully:", token)

if __name__ == "__main__":
    unittest.main()