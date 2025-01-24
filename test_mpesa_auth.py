import requests
import base64

# Your consumer key and secret
consumer_key = "lFqpIhZZpPM2WOpgyXamTMfaUiPOjR8xfaJGWXsqUGLEolY0"
consumer_secret = "eAv4eSvvK6u05KMi33vWQNkM6mfvrvGV61OgIAfgphYpEPgDvSKauGKGSInAKTUA"

# Correct URL for Safaricom sandbox
url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

# Generate Basic Auth
credentials = f"{consumer_key}:{consumer_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response = requests.post(
        url, 
        headers=headers, 
        verify=True  # SSL verification
    )
    
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.text)
    
    # Try parsing JSON
    try:
        json_response = response.json()
        print("\nJSON Response:", json_response)
    except ValueError as json_error:
        print(f"JSON Parsing Error: {json_error}")

except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")