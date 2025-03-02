import pytest
import os
from dotenv import load_dotenv
from safaricom_sdk import MPESAClient, Configuration
from safaricom_sdk.models import (
    STKPushRequest, 
    C2BRegisterURLRequest,
    C2BPaymentRequest, 
    B2CRequest
)
from safaricom_sdk.utils import (
    validate_phone_number, 
    generate_password, 
    format_timestamp
)
import base64
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()
logging.captureWarnings(True)

@pytest.fixture
def mpesa_client():
    """Create a MPESAClient for testing"""
    config = Configuration(
        consumer_key=os.getenv('MPESA_CONSUMER_KEY'),  # Load from environment variable
        consumer_secret=os.getenv('MPESA_CONSUMER_SECRET'),  # Load from environment variable
        environment=os.getenv('MPESA_ENVIRONMENT')
    )
    return MPESAClient(config)

def test_authentication(mpesa_client):
    """Test authentication and token generation"""
    try:
        # Print detailed configuration details for debugging
        print("Detailed Authentication Configuration:")
        print(f"Consumer Key: {mpesa_client.config.consumer_key}")
        print(f"Consumer Secret Length: {len(mpesa_client.config.consumer_secret)}")
        print(f"Environment: {mpesa_client.config.environment}")
        print(f"Verify SSL: {mpesa_client.config.verify_ssl}")

        # Attempt to get access token with explicit error handling
        try:
            url = 'https://apisandbox.safaricom.et/v1/token/generate?grant_type=client_credentials'
            # Use Basic Auth instead of Bearer token
            auth = HTTPBasicAuth(mpesa_client.config.consumer_key, mpesa_client.config.consumer_secret)

            # Ensure SSL verification is enabled
            response = requests.get(url, auth=auth, verify=True)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            token = response.json().get('access_token')

            # Comprehensive token validation
            assert token is not None, "Failed to generate access token: Token is None"
            assert isinstance(token, str), "Access token must be a string"
            assert len(token) > 0, "Access token cannot be empty"

            # Partially print token for security
            print(f"Successfully generated access token: {token[:10]}...")

        except Exception as auth_error:
            # Log the full traceback of authentication error
            import traceback
            print("Authentication Error Details:")
            traceback.print_exc()
            raise  # Re-raise to fail the test

    except Exception as e:
        # Final catch-all to ensure detailed error reporting
        print(f"Comprehensive Authentication Failure: {str(e)}")
        pytest.fail(f"Authentication failed: {str(e)}")

def test_stk_push(mpesa_client):
    """Test STK Push request"""
    shortcode = os.getenv('MPESA_SHORTCODE', '')
    if not shortcode:
        pytest.skip("MPESA_SHORTCODE not configured")

    stk_request = STKPushRequest(
        MerchantRequestID=mpesa_client.generate_request_id(),
        BusinessShortCode=shortcode,
        Password=base64.b64encode(f"{shortcode}bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919{format_timestamp()}".encode()).decode(),
        Timestamp=format_timestamp(),
        Amount='10',
        PartyA=validate_phone_number(os.getenv('TEST_PHONE_NUMBER', '')),
        PartyB=shortcode,
        PhoneNumber=validate_phone_number(os.getenv('TEST_PHONE_NUMBER', '')),
        TransactionDesc='Test Payment',
        CallBackURL='https://example.com/mpesa/stk_push_callback',
        AccountReference='TestPayment'
    )
    
    try:
        response = mpesa_client.stk_push(stk_request)
        print("STK Push Response:", response)
    except Exception as e:
        pytest.fail(f"STK Push error: {str(e)}")

def test_c2b_registration(mpesa_client):
    """Test C2B URL Registration with comprehensive error handling"""
    shortcode = os.getenv('MPESA_SHORTCODE_ALT')
    if not shortcode:
        pytest.skip("MPESA_SHORTCODE_ALT not configured")

    # Print out environment details for debugging
    print("C2B Registration Test Environment Details:")
    print(f"Shortcode: {shortcode}")
    print(f"Confirmation URL: https://www.myservice:8080/confirmation")
    print(f"Validation URL: https://www.myservice:8080/validation")

    c2b_register_request = C2BRegisterURLRequest(
        ShortCode=shortcode,
        ResponseType='Completed',
        ConfirmationURL='https://example.com/mpesa/c2b/confirmation',
        ValidationURL='https://example.com/mpesa/c2b/validation'
    )
    
    try:
        # Print the full request details before making the API call
        print("C2B Registration Request Details:")
        print(json.dumps(c2b_register_request.model_dump(), indent=2))

        response = mpesa_client.register_c2b_url(c2b_register_request)
        
        # Print the full response for debugging
        print("C2B Registration Response:")
        print(json.dumps(response, indent=2))

        # Flexible response validation
        assert response is not None, "Empty response received"
        
        # Check for different possible response formats
        if isinstance(response, dict):
            # Check for ResponseCode or other success indicators
            assert any(key in response for key in ['ResponseCode', 'response_text', 'success', 'status']), \
                "Response is missing expected success indicators"
        elif isinstance(response, str):
            # If it's a string response, check for success-related content
            assert any(success_indicator in response.lower() 
                       for success_indicator in ['success', 'registered', 'confirmed']), \
                "Response does not indicate successful registration"
        else:
            pytest.fail(f"Unexpected response type: {type(response)}")
        
    except Exception as e:
        # Comprehensive error logging
        print(f"C2B Registration Test Failed:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        
        # If it's an MPESAError or APIError, print additional context
        if hasattr(e, 'response_description'):
            print(f"API Response Description: {e.response_description}")
        
        # Re-raise to fail the test
        raise

def test_b2c_payment(mpesa_client):
    """Test B2C Payment"""
    shortcode = os.getenv('MPESA_SHORTCODE')
    initiator_name = os.getenv('MPESA_INITIATOR_NAME')
    security_credential = os.getenv('MPESA_SECURITY_CREDENTIAL')
    test_phone_number = os.getenv('TEST_PHONE_NUMBER')

    if not all([shortcode, initiator_name, security_credential, test_phone_number]):
        pytest.skip("One or more required environment variables are not configured")

    b2c_request = B2CRequest(
        InitiatorName=initiator_name,
        SecurityCredential=security_credential,
        Amount=100,
        PartyA=shortcode,
        PartyB=validate_phone_number(test_phone_number),
        Remarks='Test Payment',
        QueueTimeOutURL='https://example.com/mpesa/b2c/timeout',
        ResultURL='https://example.com/mpesa/b2c/result'
    )
    
    try:
        response = mpesa_client.process_b2c_payment(b2c_request)
        assert response.ResponseCode == '0', "B2C Payment failed"
    except Exception as e:
        pytest.fail(f"B2C Payment error: {str(e)}")

# Update the phone number constant
TEST_PHONE_NUMBER = '251777139917'

def test_phone_number_validation():
    """Test phone number validation utility"""
    test_numbers = [
        '251777139917',  # Your specific number
        '0777139917',    # Local format
        '+251777139917'  # International format
    ]
    
    for number in test_numbers:
        try:
            validated = validate_phone_number(number)
            assert validated == '251777139917', f"Phone number not formatted correctly: {number}"
            print(f"Validated phone number: {validated}")
        except Exception as e:
            pytest.fail(f"Phone number validation failed for {number}: {str(e)}")

# Existing imports and code...

def test_error_handling(mpesa_client):
    """Test error handling scenarios"""
    # Test with invalid credentials
    invalid_config = Configuration(
        consumer_key='invalid_key',
        consumer_secret='invalid_secret',
        environment='sandbox'
    )
    invalid_client = MPESAClient(invalid_config)
    
    with pytest.raises(Exception):
        invalid_client.auth.get_access_token()

def test_manual_stk_push(mpesa_client):
    """
    Manual test for STK Push with specific request details
    This is a diagnostic test to help troubleshoot STK Push integration
    """
    # Retrieve configuration from environment
    shortcode = os.getenv('MPESA_SHORTCODE')
    passkey = os.getenv('MPESA_PASSKEY')
    phone_number = os.getenv('TEST_PHONE_NUMBER')
    callback_url = os.getenv('CALLBACK_URL')

    # Comprehensive environment variable validation
    missing_vars = [
        var for var, value in [
            ('MPESA_SHORTCODE', shortcode),
            ('MPESA_PASSKEY', passkey),
            ('TEST_PHONE_NUMBER', phone_number),
            ('CALLBACK_URL', callback_url)
        ] if not value
    ]

    # Raise detailed error if any required variables are missing
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Comprehensive environment variable logging
    print("STK Push Test Configuration:")
    print(f"Shortcode: {shortcode}")
    print(f"Passkey: {passkey[:5]}...")  # Mask sensitive information
    print(f"Phone Number: {phone_number}")
    print(f"Callback URL: {callback_url}")
    
    try:
        # Generate timestamp (as per M-PESA requirements)
        from datetime import datetime
        import uuid
        import base64
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Generate password (Base64 of BusinessShortCode + Passkey + Timestamp)
        password_raw = f"{shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_raw.encode()).decode('utf-8')
        
        # Generate a unique MerchantRequestID
        merchant_request_id = str(uuid.uuid4())
        
        # Prepare STK Push request with correct types
        stk_push_request = STKPushRequest(
            BusinessShortCode=str(shortcode),
            Password=password,
            Timestamp=timestamp,
            TransactionType="CustomerBuyGoodsOnline",
            Amount=str(50),  # Convert to string
            PartyA=str(shortcode),
            PartyB=str(600000),
            PhoneNumber=phone_number,
            CallBackURL=callback_url,
            AccountReference="goods sales",
            TransactionDesc="Monthly goods Package payment",
            MerchantRequestID=merchant_request_id
        )
        
        # Print out request details for debugging
        print("Manual STK Push Request Details:")
        print(json.dumps(stk_push_request.model_dump(), indent=2))
        
        # Perform STK Push
        response = mpesa_client.stk_push(stk_push_request)
        
        # Print response for debugging
        print("\nSTK Push Response:")
        print(json.dumps(response.model_dump(), indent=2))
        
        # Validate response
        assert response is not None, "Empty STK Push response"
        assert hasattr(response, 'MerchantRequestID'), "Response missing MerchantRequestID"
        assert hasattr(response, 'CheckoutRequestID'), "Response missing CheckoutRequestID"
        
    except Exception as e:
        # Comprehensive error logging
        print(f"Manual STK Push Test Failed:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        
        # If it's an MPESAError, print additional context
        if hasattr(e, 'response_description'):
            print(f"API Response Description: {e.response_description}")
        
        # Re-raise to fail the test
        raise
