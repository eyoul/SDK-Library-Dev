import os
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator
import requests
import base64

class Configuration(BaseModel):
    """Configuration class for the Safaricom M-PESA SDK"""
    
    consumer_key: str = os.getenv('MPESA_CONSUMER_KEY', '')
    consumer_secret: str = os.getenv('MPESA_CONSUMER_SECRET', '')
    environment: str = os.getenv('MPESA_ENVIRONMENT', 'sandbox')
    timeout: int = 30
    max_retries: int = 3
    app_name: str = os.getenv('APP_NAME', 'EyuApp')
    verify_ssl: bool = True

    # Validation to ensure credentials are provided
    @field_validator('consumer_key', 'consumer_secret')
    @classmethod
    def validate_credentials(cls, v, info):
        if not v:
            raise ValueError(f"{info.field_name} must be set in environment variables. "
                             "Please check your .env file or set MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET.")
        return v

    # API endpoints
    base_url: HttpUrl = "https://developer.safaricom.et/apps"  # Ensure this is correct for production
    auth_url: str = "/v1/oauth2/token"
    stkpush_url: str = "/mpesa/stkpush/v3/processrequest"
    b2c_url: str = "/mpesa/b2c/v1/paymentrequest"
    c2b_register_url: str = "/v1/c2b-registerurl/register"
    c2b_payment_url: str = "/v1/c2b/payments"
    
    # Optional configurations
    api_key: Optional[str] = None  # Update if you have an API key
    initiator_name: Optional[str] = None
    security_credential: Optional[str] = None
    
    @property
    def is_production(self) -> bool:
        """Check if environment is production"""
        return self.environment.lower() == "production"
    
    def get_auth_url(self) -> str:
        """Get the complete authentication URL"""
        return f"{self.base_url}{self.auth_url}"
    
    def get_stkpush_url(self) -> str:
        """Get the complete STK push URL"""
        return f"{self.base_url}{self.stkpush_url}"
    
    def get_b2c_url(self) -> str:
        """Get the complete B2C URL"""
        return f"{self.base_url}{self.b2c_url}"
    
    def get_c2b_register_url(self) -> str:
        """Get the complete C2B registration URL"""
        return f"{self.base_url}{self.c2b_register_url}"
    
    def get_c2b_payment_url(self) -> str:
        """Get the complete C2B payment URL"""
        return f"{self.base_url}{self.c2b_payment_url}"

    def get_access_token(self):
        """Get access token from Safaricom API"""
        url = f"{self.base_url}{self.auth_url}"
        
        # Use base64 encoded credentials
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        payload = "grant_type=client_credentials"

        try:
            response = requests.request(
                "POST", 
                url, 
                headers=headers, 
                data=payload,
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise an error for bad responses
            
            # Log the response for debugging
            print(f"Access Token Response: {response.text}")
            
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching access token: {str(e)}")
            print(f"Response content: {response.text}")
            return None

# Example of calling the method
# config = Configuration()
# token = config.get_access_token()
# print(token)
