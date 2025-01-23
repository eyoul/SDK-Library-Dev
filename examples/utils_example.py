import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from safaricom_sdk.utils import (
    validate_phone_number, 
    generate_password, 
    format_timestamp,
    setup_logging
)

def demonstrate_phone_validation():
    """Demonstrate phone number validation with comprehensive testing"""
    test_cases = [
        # Valid Ethiopian phone numbers in different formats
        '0777139917',   # Local format
        '+251777139917',  # International format
        '251777139917',   # Full country code
        
        # Edge cases and potential error scenarios
        '0712345678',   # Another valid Ethiopian number
        '+251712345678'  # Another international format
    ]
    
    for number in test_cases:
        try:
            validated = validate_phone_number(number)
            print(f"✅ Original: {number}, Validated: {validated}")
        except ValueError as e:
            print(f"❌ Error validating {number}: {e}")

def demonstrate_password_generation():
    """
    Demonstrate password generation with secure practices
    
    Uses environment variables for sensitive information
    Handles potential errors gracefully
    """
    try:
        # Retrieve credentials from environment variables
        shortcode = os.getenv('MPESA_SHORTCODE', '600000')
        passkey = os.getenv('MPESA_PASSKEY')
        
        # Validate passkey
        if not passkey:
            print("⚠️ Warning: MPESA_PASSKEY not set. Using placeholder.")
            passkey = 'your_safaricom_passkey'
        
        # Generate timestamp
        current_timestamp = format_timestamp()
        
        # Generate password
        password = generate_password(
            shortcode=shortcode, 
            passkey=passkey, 
            timestamp=current_timestamp
        )
        
        print(f"🔐 Generated Password Details:")
        print(f"   Shortcode: {shortcode}")
        print(f"   Timestamp: {current_timestamp}")
        print(f"   Password: {password}")
        
    except ValueError as e:
        print(f"❌ Password generation error: {e}")

def main():
    # Configure logging
    logger = setup_logging(
        level=logging.DEBUG, 
        log_file='mpesa_sdk_examples.log'
    )
    
    print("🔍 Demonstrating Phone Number Validation:")
    demonstrate_phone_validation()
    
    print("\n🔐 Demonstrating Password Generation:")
    demonstrate_password_generation()

if __name__ == '__main__':
    main()