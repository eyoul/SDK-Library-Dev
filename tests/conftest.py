import os
import pytest
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
load_dotenv('test.env')

@pytest.fixture(scope='session')
def mpesa_client(request):
    # Import here to avoid circular imports
    from safaricom_sdk.client import MPESAClient
    from safaricom_sdk.config import Configuration

    # Create configuration using environment variables
    config = Configuration(
        consumer_key=os.getenv('MPESA_CONSUMER_KEY'),
        consumer_secret=os.getenv('MPESA_CONSUMER_SECRET'),
        environment='sandbox'
    )
    
    return MPESAClient(config)