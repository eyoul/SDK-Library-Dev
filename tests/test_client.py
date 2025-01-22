import unittest
from unittest.mock import patch, MagicMock
from safaricom_sdk.client import MPESAClient
from safaricom_sdk.config import Configuration
from safaricom_sdk.models import STKPushRequest, C2BPaymentRequest, B2CRequest
from safaricom_sdk.exceptions import MPESAError

class TestMPESAClient(unittest.TestCase):

    def setUp(self):
        self.config = Configuration(
            consumer_key='iYCMIkGY4jMlnXtVlybcZaZW7J2LybD11VGs6aI5MJbKuT8Q',
            consumer_secret='Ld5Y9KJiLFNnGG5ceVNWxXp3tW1AYpZP7k6IG6kMQOpyEKOl43aKiYmjOxoPXglY',
            environment='sandbox'  # Use sandbox for testing
        )
        self.client = MPESAClient(self.config)

    @patch('safaricom_sdk.client.requests.request')
    def test_stk_push(self, mock_request):
        mock_response = {
            "MerchantRequestID": "test_request_id",
            "CheckoutRequestID": "mock_checkout_request_id",
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "CustomerMessage": "Request accepted"
        }
        mock_request.return_value = MagicMock(status_code=200, json=lambda: mock_response)

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
        self.assertEqual(response.ResponseCode, '0')

    @patch('safaricom_sdk.client.requests.request')
    def test_process_c2b_payment(self, mock_request):
        mock_response = {
            "ResponseCode": "0",
            "ResponseDescription": "Success"
        }
        mock_request.return_value = MagicMock(status_code=200, json=lambda: mock_response)

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
        self.assertEqual(response.ResponseCode, '0')

    @patch('safaricom_sdk.client.requests.request')
    def test_process_b2c_payment(self, mock_request):
        mock_response = {
            "ResponseCode": "0",
            "ResponseDescription": "Success"
        }
        mock_request.return_value = MagicMock(status_code=200, json=lambda: mock_response)

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
        self.assertEqual(response.ResponseCode, '0')

    @patch('safaricom_sdk.client.requests.request')
    def test_stk_push_failure(self, mock_request):
        mock_response = {
            "errorCode": "400",
            "errorMessage": "Bad Request"
        }
        mock_request.return_value = MagicMock(status_code=400, json=lambda: mock_response)

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