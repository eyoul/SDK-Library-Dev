import base64
from datetime import datetime, timedelta
import requests
from typing import Optional, Dict
from .exceptions import MPESAError
from .config import Configuration
import json

class Authentication:
    """Authentication handler for Safaricom M-PESA API"""    
    def __init__(self, config: Configuration):
        self.config = config
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
    
    def _generate_basic_auth(self) -> str:
        """Generate Basic Auth string from consumer key and secret"""
        credentials = f"{self.config.consumer_key}:{self.config.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        if not self._is_token_valid():
            self._refresh_access_token()
        return self._access_token
    
    def _is_token_valid(self) -> bool:
        """Check if current access token is valid"""
        if not self._access_token or not self._token_expiry:
            return False
        return datetime.now() < self._token_expiry
    
    def _refresh_access_token(self) -> None:
        """Refresh the access token with comprehensive error handling"""
        # Use the correct Safaricom sandbox token generation URL
        url = 'https://apisandbox.safaricom.et/v1/token/generate?grant_type=client_credentials'

        # Validate credentials before making the request
        if not self.config.consumer_key or not self.config.consumer_secret:        
            raise MPESAError("Consumer key or secret is missing")

        headers = {
            'Authorization': self._generate_basic_auth()
        }

        try:
            # Use requests.request for more control and detailed logging
            response = requests.request(
                method='GET',
                url=url,
                headers=headers,
                verify=self.config.verify_ssl,
                timeout=15  # Increased timeout
            )

            # Handle mocked responses in tests
            raw_content = response.text if isinstance(response.text, (str, bytes)) else response.text()

            # Parse the response
            parsed_content = json.loads(raw_content)

            # Update access token and expiry
            self._access_token = parsed_content.get('access_token')
            if not self._access_token:
                raise MPESAError("Failed to retrieve access token")

            # Set token expiry
            expiry_seconds = int(parsed_content.get('expires_in', 3600))
            self._token_expiry = datetime.now() + timedelta(seconds=expiry_seconds)

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise MPESAError(f"Failed to refresh access token: {str(e)}")

    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication for API requests"""
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }
