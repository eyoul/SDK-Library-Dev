from typing import Optional
from pydantic import BaseModel, HttpUrl
import requests

class Configuration(BaseModel):
    """Configuration class for the Safaricom M-PESA SDK"""
    
    consumer_key: str = 'iYCMIkGY4jMlnXtVlybcZaZW7J2LybD11VGs6aI5MJbKuT8Q'  # Your Consumer Key
    consumer_secret: str = 'Ld5Y9KJiLFNnGG5ceVNWxXp3tW1AYpZP7k6IG6kMQOpyEKOl43aKiYmjOxoPXglY'  # Your Consumer Secret
    environment: str = "sandbox"  # Set to production
    timeout: int = 30
    max_retries: int = 3
    app_name: str = 'Testapp'  # Application name
    verify_ssl: bool = True  # Add SSL verification flag

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
        url = "https://sandbox.saf.et/oauth/v1/generate"
        querystring = {"grant_type": "client_credentials"}
        payload = ""
        headers = {
            "Authorization": "EaGFMFzk72snYQQlmcDaiyvikjBF8R12HsHTcczzdSYJlm0HO01w3E28v1SXPIne8U3qMgi0d3esOd4rFfw0G244HatJUQH4BggUQpT0oqD2K9PJmg8CkhxN7xqlRkX13d6WM9gcQjEzRF1AdXAxI5GB0eYgJ4md7DI9XtumXHMmlOqNSs6LuQf/VpQ+zBPX7dCaHMz4blmghSxtXYBOFM9+1uJYv9y3vVVKGG+/bwyYXKXtBFRMMB3tiV52/sDh1EgP1CaeaOArNJSJDl20aQSVHsJpeT+JpOEu33a/Pj+jycoFZ6z8epEg+Uu49FDt0EG7mi/4kyCZRambv9G0/Q=="
        }

        try:
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching access token: {str(e)}")
            return None

# Example of calling the method
# config = Configuration()
# token = config.get_access_token()
# print(token)
