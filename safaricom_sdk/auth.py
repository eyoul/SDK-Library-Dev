import base64
from datetime import datetime, timedelta
import requests
from typing import Optional, Dict
from .exceptions import MPESAError
from .config import Configuration

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
        """Refresh the access token"""
        headers = {
            "Authorization": self._generate_basic_auth()
        }
        
        params = {
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.get(
                self.config.get_auth_url(),
                headers=headers,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data["access_token"]
            self._token_expiry = datetime.now() + timedelta(seconds=int(data["expires_in"]))
            
        except requests.exceptions.RequestException as e:
            raise MPESAError(f"Authentication failed: {str(e)}")
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication for API requests"""
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }
