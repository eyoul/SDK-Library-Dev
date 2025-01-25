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

# Load environment variables
load_dotenv()

@pytest.fixture
def mpesa_client():
    """Create a MPESAClient for testing"""
    config = Configuration(
        consumer_key=os.getenv('MPESA_CONSUMER_KEY'),  # Load from environment variable
        consumer_secret=os.getenv('MPESA_CONSUMER_SECRET'),  # Load from environment variable
        environment='sandbox'
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
            token = mpesa_client.auth.get_access_token()
            
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
    """Test C2B URL Registration"""
    shortcode = os.getenv('MPESA_SHORTCODE')
    if not shortcode:
        pytest.skip("MPESA_SHORTCODE not configured")

    c2b_register_request = C2BRegisterURLRequest(
        ShortCode=shortcode,
        ResponseType='Completed',
        ConfirmationURL='https://example.com/mpesa/c2b/confirmation',
        ValidationURL='https://example.com/mpesa/c2b/validation'
    )
    
    try:
        response = mpesa_client.register_c2b_url(c2b_register_request)
        assert 'ResponseCode' in response, "C2B Registration failed"
    except Exception as e:
        pytest.fail(f"C2B Registration error: {str(e)}")

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

# Add your new test functions here