import json
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

import requests
import pytest

from safaricom_sdk.client import MPESAClient
from safaricom_sdk.config import Configuration
from safaricom_sdk.exceptions import MPESAError
from safaricom_sdk.models import (
    STKPushRequest, 
    C2BPaymentRequest, 
    B2CRequest
)

class TestMPESAClient(unittest.TestCase):
    def setUp(self):
        # Create a configuration with test credentials
        self.config = Configuration(
            consumer_key='test_key', 
            consumer_secret='test_secret', 
            timeout=5
        )
        # Initialize the client for all tests
        self.client = MPESAClient(self.config)

        # Patch the _refresh_access_token method to set a mock token
        def mock_refresh_token(self):
            self._access_token = "mock_access_token_for_tests"
            self._token_expiry = datetime.now() + timedelta(hours=1)

        # Apply the patch
        self.client.auth._refresh_access_token = mock_refresh_token.__get__(self.client.auth)

    @patch('safaricom_sdk.client.requests.request')
    def test_stk_push(self, mock_request):
        # Mock the STK push response with full model
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "MerchantRequestID": "test_request_id",
            "CheckoutRequestID": "mock_checkout_request_id",
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "CustomerMessage": "Request accepted"
        })
        mock_request.return_value = mock_response

        request = STKPushRequest(
            MerchantRequestID='test_request_id',
            BusinessShortCode='your_business_shortcode',
            Password='your_generated_password',
            Timestamp='your_timestamp',
            Amount='100',
            PartyA='your_phone_number',
            PartyB='your_shortcode',
            TransactionDesc='Payment for testing',
            CallBackURL='your_callback_url',
            AccountReference='your_account_reference',
            PhoneNumber='+251712870937'  # Ensure PhoneNumber is a string
        )
    
        response = self.client.stk_push(request)  # Pass the request object directly
        self.assertEqual(response.ResponseCode, "0")

    @patch('safaricom_sdk.client.requests.request')
    def test_process_c2b_payment(self, mock_request):
        # Mock the C2B payment response with full model
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "ConversationID": "test_conversation_id",
            "OriginatorConversationID": "test_originator_id",
            "TransactionID": "test_transaction_id"
        })
        mock_request.return_value = mock_response

        request = C2BPaymentRequest(
            RequestRefID='test_ref_id',
            CommandID='PayBill',
            Remark='Payment for testing',
            ChannelSessionID='session_id',
            SourceSystem='test_system',
            Timestamp='2025-01-22T00:00:00',
            Parameters=[],
            Initiator={"IdentifierType": 1, "Identifier": "initiator_id", "SecurityCredential": "security_credential"},
            PrimaryParty={"IdentifierType": 1, "Identifier": "primary_party_id"},
            ReceiverParty={"IdentifierType": 1, "Identifier": "receiver_party_id"}
        )

        response = self.client.process_c2b_payment(request)  # Pass the request object directly
        self.assertEqual(response.ResponseCode, "0")

    @patch('safaricom_sdk.client.requests.request')
    def test_process_b2c_payment(self, mock_request):
        # Mock the B2C payment response with full model
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "ConversationID": "test_conversation_id",
            "OriginatorConversationID": "test_originator_id",
            "TransactionID": "test_transaction_id"
        })
        mock_request.return_value = mock_response

        request = B2CRequest(
            InitiatorName='your_initiator_name',
            SecurityCredential='your_security_credential',
            Amount=100,
            PartyA='your_business_shortcode',
            PartyB='recipient_phone_number',
            Remarks='Payment for testing',
            QueueTimeOutURL='your_timeout_url',
            ResultURL='your_result_url'
        )

        response = self.client.process_b2c_payment(request)  # Pass the request object directly
        self.assertEqual(response.ResponseCode, "0")

    @patch('safaricom_sdk.client.requests.request')
    def test_stk_push_failure(self, mock_request):
        # Mock a failure response for STK push
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({
            "errorCode": "400",
            "errorMessage": "Bad Request"
        })
        mock_request.return_value = mock_response

        request = STKPushRequest(
            MerchantRequestID='test_request_id',
            BusinessShortCode='your_business_shortcode',
            Password='your_generated_password',
            Timestamp='your_timestamp',
            Amount='100',
            PartyA='your_phone_number',
            PartyB='your_shortcode',
            TransactionDesc='Payment for testing',
            CallBackURL='your_callback_url',
            AccountReference='your_account_reference',
            PhoneNumber='+251712870937'  # Ensure PhoneNumber is a string
        )

        with self.assertRaises(MPESAError):
            self.client.stk_push(request)  # Pass the request object directly

if __name__ == '__main__':
    unittest.main()