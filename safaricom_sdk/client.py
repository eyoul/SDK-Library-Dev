import json
from typing import Dict, Any, Optional
import requests
from datetime import datetime
import uuid

from .config import Configuration
from .auth import Authentication
from .models import (
    STKPushRequest, STKPushResponse,
    C2BRegisterURLRequest, C2BPaymentRequest,
    B2CRequest, TransactionResponse
)
from .exceptions import MPESAError, APIError

class MPESAClient:
    """Main client for interacting with M-PESA APIs"""
    
    def __init__(self, config: Configuration):
        self.config = config
        self.auth = Authentication(config)
    
    def _make_request(self, method: str, url: str, data: Optional[Dict] = None, verify_ssl: bool = False) -> Dict:
        """Make HTTP request to M-PESA API"""
        headers = self.auth.get_headers()

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=self.config.timeout,
                verify=verify_ssl  # Set to False for testing
            )

            response_data = response.json()

            if response.status_code >= 400:
                raise APIError(
                    message=f"API request failed: {response.status_code}",
                    response_code=response_data.get("errorCode"),
                    response_description=response_data.get("errorMessage")
                )

            return response_data

        except requests.exceptions.RequestException as e:
            raise MPESAError(f"Request failed: {str(e)}")

    def stk_push(self, request: STKPushRequest) -> STKPushResponse:
        """Initiate STK Push request"""
        url = self.config.get_stkpush_url()
        response = self._make_request("POST", url, request.model_dump())
        return STKPushResponse(**response)
    
    def register_c2b_url(self, request: C2BRegisterURLRequest) -> Dict[str, Any]:
        """Register C2B URLs"""
        url = f"{self.config.get_c2b_register_url()}?apikey={self.config.api_key}"
        return self._make_request("POST", url, request.dict())
    
    def process_c2b_payment(self, request: C2BPaymentRequest) -> TransactionResponse:
        """Process C2B payment"""
        url = self.config.get_c2b_payment_url()
        response = self._make_request("POST", url, request.model_dump())
        return TransactionResponse(**response)
    
    def process_b2c_payment(self, request: B2CRequest) -> TransactionResponse:
        """Process B2C payment"""
        url = self.config.get_b2c_url()
        response = self._make_request("POST", url, request.model_dump())
        return TransactionResponse(**response)
    
    @staticmethod
    def generate_timestamp() -> str:
        """Generate timestamp in required format"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def generate_request_id() -> str:
        """Generate unique request ID"""
        return str(uuid.uuid4())
