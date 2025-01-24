import logging
import re
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import base64

# Configure default logger
logger = logging.getLogger(__name__)

def setup_logging(
    level: int = logging.INFO, 
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure comprehensive logging with optional file output
    
    Args:
        level (int): Logging level (default: logging.INFO)
        log_file (str, optional): Path to log file for persistent logging
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create or get logger
    logger = logging.getLogger('safaricom_sdk')
    logger.setLevel(level)
    
    # Clear existing handlers to prevent duplicate logging
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except IOError as e:
            logger.error(f"Could not create log file: {e}")
    
    return logger

def validate_phone_number(phone_number: str) -> str:
    """
    Validate and standardize Ethiopian phone numbers
    
    Supports formats:
    - 0712345678 (local)
    - +251712345678 (international)
    - 251712345678 (full country code)
    
    Args:
        phone_number (str): Phone number to validate
    
    Returns:
        str: Standardized phone number with 251 country code
    
    Raises:
        ValueError: If phone number is invalid
    """
    # Remove any non-digit characters
    cleaned = re.sub(r'\D', '', phone_number)
    
    # Validate basic length and prefix
    if len(cleaned) < 9 or len(cleaned) > 12:
        raise ValueError(f"Invalid phone number length: {phone_number}")
    
    # Standardize to full international format
    if cleaned.startswith('0'):
        cleaned = '251' + cleaned[1:]
    elif cleaned.startswith('9'):
        cleaned = '251' + cleaned
    elif not cleaned.startswith('251'):
        cleaned = '251' + cleaned[-9:]
    
    # Final validation for Ethiopian mobile numbers
    if not re.match(r'^251(9|7)\d{8}$', cleaned):
        raise ValueError(f"Invalid Ethiopian phone number format: {phone_number}")
    
    return cleaned

def format_amount(amount: float) -> str:
    """
    Format amount to string with 2 decimal places
    
    Args:
        amount (float): Amount to format
    
    Returns:
        str: Formatted amount with 2 decimal places
    """
    return "{:.2f}".format(amount)

def generate_password(
    shortcode: str, 
    passkey: str, 
    timestamp: Optional[str] = None
) -> str:
    """
    Generate base64 encoded password for STK Push
    
    Args:
        shortcode (str): Business shortcode
        passkey (str): Safaricom passkey
        timestamp (str, optional): Timestamp in YYYYMMDDHHMMSS format
    
    Returns:
        str: Base64 encoded password
    """
    if timestamp is None:
        timestamp = format_timestamp()
    
    # Validate inputs
    if not shortcode or not passkey:
        raise ValueError("Shortcode and passkey must not be empty")
    
    password_str = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(password_str.encode()).decode()

def log_api_response(
    response: Dict[str, Any], 
    operation: str = "API Request"
) -> None:
    """
    Log API response with context and appropriate logging level
    
    Args:
        response (Dict[str, Any]): API response dictionary
        operation (str, optional): Description of the API operation
    """
    # Determine log level based on response code
    log_method = logger.info if response.get("ResponseCode") == "0" else logger.error
    
    # Log with detailed information
    log_method(
        "%s Details: "
        "ResponseCode=%s, "
        "Description=%s, "
        "Full Response=%s", 
        operation, 
        response.get("ResponseCode", "N/A"),
        response.get("ResponseDescription", "No description"),
        response
    )

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime to Safaricom required timestamp format
    
    Args:
        dt (datetime, optional): Datetime to format. 
                                 Defaults to current time if not provided.
    Returns:
        str: Formatted timestamp in YYYYMMDDHHMMSS format
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("%Y%m%d%H%M%S")

def sanitize_input(input_value: str, max_length: int = 100) -> str:
    """
    Sanitize input to prevent injection and limit length
    
    Args:
        input_value (str): Input to sanitize
        max_length (int, optional): Maximum allowed length
    
    Returns:
        str: Sanitized input
    """
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>&\'"()]', '', str(input_value))
    
    # Truncate to max length
    return sanitized[:max_length]

# Optional: Configure default logging when module is imported
setup_logging()