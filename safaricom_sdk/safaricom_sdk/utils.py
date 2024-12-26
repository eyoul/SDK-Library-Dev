import logging
from typing import Any, Dict
from datetime import datetime
import base64

# Configure logging
logger = logging.getLogger(__name__)

def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_phone_number(phone_number: str) -> str:
    """Validate and format phone number"""
    # Remove any spaces or special characters
    cleaned = ''.join(filter(str.isdigit, phone_number))
    
    # Ensure it starts with country code
    if not cleaned.startswith('251'):
        if cleaned.startswith('0'):
            cleaned = '251' + cleaned[1:]
        else:
            cleaned = '251' + cleaned
    
    if len(cleaned) != 12:
        raise ValueError("Invalid phone number length")
    
    return cleaned

def format_amount(amount: float) -> str:
    """Format amount to string with 2 decimal places"""
    return "{:.2f}".format(amount)

def generate_password(shortcode: str, passkey: str, timestamp: str) -> str:
    """Generate password for STK Push"""
    password_str = shortcode + passkey + timestamp
    return base64.b64encode(password_str.encode()).decode()

def log_api_response(response: Dict[str, Any]) -> None:
    """Log API response with appropriate level"""
    if response.get("ResponseCode") == "0":
        logger.info("API request successful: %s", response)
    else:
        logger.error("API request failed: %s", response)

def format_timestamp(dt: datetime = None) -> str:
    """Format datetime to required timestamp format"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y%m%d%H%M%S")
