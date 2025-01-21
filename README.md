# Safaricom M-PESA SDK

A Python SDK for integrating with Safaricom M-PESA APIs. This SDK provides a simple and intuitive way to interact with various M-PESA services including STK Push, C2B, and B2C payments.

## Features

- Easy configuration and setup
- Authentication handling with automatic token refresh
- Support for all major M-PESA APIs:
  - STK Push (NI Push)
  - Customer to Business (C2B)
  - Business to Customer (B2C)
- Comprehensive error handling
- Type hints and validation using Pydantic
- Detailed logging
- Extensive documentation

## Installation

```bash
pip install requests
pip install safaricom-sdk
```

## Quick Start

```python
from safaricom_sdk import MPESAClient, Configuration

# Initialize configuration
config = Configuration(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    environment="sandbox"  # or "production"
)

# Create client instance
client = MPESAClient(config)

# Example: STK Push request
from safaricom_sdk.models import STKPushRequest

stk_request = STKPushRequest(
    MerchantRequestID="test-123",
    BusinessShortCode="174379",
    Password="your_password",
    Timestamp="20240101120000",
    TransactionType="CustomerPayBillOnline",
    Amount="1.00",
    PartyA="254712345678",
    PartyB="174379",
    PhoneNumber="254712345678",
    TransactionDesc="Test Payment",
    CallBackURL="https://your-callback-url.com/callback",
    AccountReference="Test"
)

response = client.stk_push(stk_request)
print(response.dict())
```

## Documentation

### Configuration

The SDK can be configured with various options:

```python
config = Configuration(
    consumer_key="your_key",
    consumer_secret="your_secret",
    environment="sandbox",  # or "production"
    timeout=30,  # request timeout in seconds
    max_retries=3  # maximum number of retry attempts
)
```

### Available APIs

1. STK Push (NI Push)
```python
response = client.stk_push(stk_request)
```

2. C2B URL Registration
```python
response = client.register_c2b_url(c2b_register_request)
```

3. C2B Payment
```python
response = client.process_c2b_payment(c2b_payment_request)
```

4. B2C Payment
```python
response = client.process_b2c_payment(b2c_request)
```

### Error Handling

The SDK provides custom exceptions for different types of errors:

- `MPESAError`: Base exception for all SDK errors
- `ConfigurationError`: Configuration-related errors
- `AuthenticationError`: Authentication failures
- `APIError`: API request failures
- `ValidationError`: Data validation errors

### Utilities

The SDK includes various utility functions:

- Phone number validation and formatting
- Amount formatting
- Password generation
- Timestamp formatting
- Logging setup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.
