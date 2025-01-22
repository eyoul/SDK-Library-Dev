# tests/test_utils.py
import unittest
from datetime import datetime
import base64
import logging
from safaricom_sdk.utils import (
    validate_phone_number,
    format_amount,
    generate_password,
    format_timestamp
)

class TestUtils(unittest.TestCase):
    def test_validate_phone_number(self):
        # Test valid phone numbers
        self.assertEqual(validate_phone_number('0712870937'), '251712870937')
        self.assertEqual(validate_phone_number('712870937'), '251712870937')
        self.assertEqual(validate_phone_number('251712870937'), '251712870937')
        
        # Test invalid phone numbers
        with self.assertRaises(ValueError):
            validate_phone_number('123')  # Too short
        with self.assertRaises(ValueError):
            validate_phone_number('251712870937123')  # Too long

    def test_format_amount(self):
        self.assertEqual(format_amount(100), '100.00')
        self.assertEqual(format_amount(100.5), '100.50')
        self.assertEqual(format_amount(100.555), '100.56')

    def test_generate_password(self):
        shortcode = '174379'
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        timestamp = '20230418163442'
        
        # Manually calculate expected base64 encoded password
        password_str = shortcode + passkey + timestamp
        expected_password = base64.b64encode(password_str.encode()).decode()
        
        self.assertEqual(
            generate_password(shortcode, passkey, timestamp), 
            expected_password
        )

    def test_format_timestamp(self):
        # Test with specific datetime
        test_datetime = datetime(2023, 4, 18, 16, 34, 42)
        self.assertEqual(
            format_timestamp(test_datetime), 
            '20230418163442'
        )
        
        # Test with default (current time)
        current_timestamp = format_timestamp()
        self.assertTrue(len(current_timestamp) == 14)
        self.assertTrue(current_timestamp.isdigit())

if __name__ == '__main__':
    unittest.main()