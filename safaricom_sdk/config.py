from typing import Optional
from pydantic import BaseModel, HttpUrl

class Configuration(BaseModel):
    """Configuration class for the Safaricom M-PESA SDK"""
    
    consumer_key: str = 'iYCMIkGY4jMlnXtVlybcZaZW7J2LybD11VGs6aI5MJbKuT8Q'  # Your Consumer Key
    consumer_secret: str = 'Ld5Y9KJiLFNnGG5ceVNWxXp3tW1AYpZP7k6IG6kMQOpyEKOl43aKiYmjOxoPXglY'  # Your Consumer Secret
    environment: str = "sandbox"  # Set to production
    timeout: int = 30
    max_retries: int = 3
    app_name: str = 'Testapp'  # Application name

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
