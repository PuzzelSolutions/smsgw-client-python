"""Basic example of sending SMS using the Puzzel SMS Gateway Python Client (Kiota).

This example demonstrates the simplest way to send an SMS message.
"""

import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message


async def send_basic_sms():
    """Send a basic SMS message."""
    
    # Configuration - Replace with your actual values
    BASE_URL = "https://smsgw.puzzel.com"
    SERVICE_ID = 12345  # Your Puzzel service ID
    USERNAME = "your_username"  # Your Puzzel username
    PASSWORD = "your_password"  # Your Puzzel password
    RECIPIENT = "+47xxxxxxxxx"  # Phone number with country code
    
    # Setup client
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = BASE_URL
    
    client = MtHttpClient(request_adapter)
    
    # Create request
    request = GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        message=[
            Message(
                recipient=RECIPIENT,
                content="Hello from Puzzel SMS Gateway!"
            )
        ]
    )
    
    # Send message
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        print(f"✓ SMS sent successfully!")
        print(f"Batch Reference: {response.batch_reference}")
        
        for status in response.message_status:
            print(f"\nMessage Details:")
            print(f"  Message ID: {status.message_id}")
            print(f"  Recipient: {status.recipient}")
            print(f"  Status Code: {status.status_code}")
            print(f"  Status Message: {status.status_message}")
            
    except Exception as e:
        print(f"✗ Failed to send SMS: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(send_basic_sms())
