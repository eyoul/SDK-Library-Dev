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

# Load environment variables
load_dotenv()

@pytest.fixture
def mpesa_client():
    """Create a MPESAClient for testing"""
    config = Configuration(
        consumer_key='lFqpIhZZpPM2WOpgyXamTMfaUiPOjR8xfaJGWXsqUGLEolY0',
        consumer_secret='eAv4eSvvK6u05KMi33vWQNkM6mfvrvGV61OgIAfgphYpEPgDvSKauGKGSInAKTUA',
        environment='sandbox'
    )
    return MPESAClient(config)

def test_authentication(mpesa_client):
    """Test authentication and token generation"""
    try:
        token = mpesa_client.auth.get_access_token()
        assert token is not None, "Failed to generate access token"
    except Exception as e:
        pytest.fail(f"Authentication failed: {str(e)}")

def test_stk_push(mpesa_client):
    """Test STK Push request"""
    stk_request = STKPushRequest(
        MerchantRequestID=mpesa_client.generate_request_id(),
        BusinessShortCode='YOUR_BUSINESS_SHORTCODE',  # Replace with actual shortcode
        Password='YOUR_PASSWORD',  # Generate or replace with actual password
        Timestamp=format_timestamp(),
        Amount='10',
        PartyA=validate_phone_number(TEST_PHONE_NUMBER),
        PartyB='YOUR_BUSINESS_SHORTCODE',  # Replace with actual shortcode
        PhoneNumber=validate_phone_number(TEST_PHONE_NUMBER),
        TransactionDesc='Test Payment',
        CallBackURL='https://your-callback-url.com/mpesa',
        AccountReference='TestPayment'
    )
    
    try:
        response = mpesa_client.stk_push(stk_request)
        print("STK Push Response:", response)
    except Exception as e:
        pytest.fail(f"STK Push error: {str(e)}")

def test_c2b_registration(mpesa_client):
    """Test C2B URL Registration"""
    c2b_register_request = C2BRegisterURLRequest(
        ShortCode=os.getenv('MPESA_SHORTCODE'),
        ResponseType='Completed',
        ConfirmationURL='https://your-confirmation-url.com/c2b',
        ValidationURL='https://your-validation-url.com/c2b'
    )
    
    try:
        response = mpesa_client.register_c2b_url(c2b_register_request)
        assert 'ResponseCode' in response, "C2B Registration failed"
    except Exception as e:
        pytest.fail(f"C2B Registration error: {str(e)}")

def test_b2c_payment(mpesa_client):
    """Test B2C Payment"""
    b2c_request = B2CRequest(
        InitiatorName=os.getenv('MPESA_INITIATOR_NAME'),
        SecurityCredential=os.getenv('MPESA_SECURITY_CREDENTIAL'),
        Amount=100,
        PartyA=os.getenv('MPESA_SHORTCODE'),
        PartyB=validate_phone_number(os.getenv('TEST_PHONE_NUMBER')),
        Remarks='Test Payment',
        QueueTimeOutURL='https://your-timeout-url.com/b2c',
        ResultURL='https://your-result-url.com/b2c'
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