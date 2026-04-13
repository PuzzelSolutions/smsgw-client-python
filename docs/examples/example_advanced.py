"""Advanced example of sending SMS with all configuration options.

This example demonstrates:
- Scheduled message delivery (send window)
- Custom originator (sender ID)
- Priority and validity settings
- Premium SMS with pricing
- Custom parameters
"""

import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message
from src.models.settings import Settings
from src.models.send_window import SendWindow
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType
from src.models.gas_settings import GasSettings
from src.models.parameter import Parameter


async def send_advanced_sms():
    """Send an SMS with advanced configuration."""
    
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
    
    # Create advanced message with all settings
    request = GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        batch_reference="advanced-example-batch",
        message=[
            Message(
                recipient=RECIPIENT,
                content="This is an advanced SMS with custom settings",
                price=100,  # Price in cents/øre (optional, for premium SMS)
                client_reference="msg-ref-12345",
                settings=Settings(
                    # Priority: 1=highest, 2=normal, 3=lowest
                    priority=1,
                    
                    # Validity: How long to try delivery (in minutes)
                    validity=173,
                    
                    # Differentiator: Group messages together
                    differentiator="marketing-campaign-2026",
                    
                    # Invoice node: For cost tracking
                    invoice_node="marketing-department",
                    
                    # Age restriction
                    age=18,
                    
                    # Session management
                    new_session=True,
                    session_id="session-abc123",
                    
                    # Encoding
                    auto_detect_encoding=True,
                    
                    # Custom originator (sender ID)
                    originator_settings=OriginatorSettings(
                        originator="MyCompany",  # Can be alphanumeric, short code, or phone number
                        originator_type=OriginatorType.Alphanumeric
                    ),
                    
                    # GAS settings for premium SMS
                    gas_settings=GasSettings(
                        service_code="02001",
                        description="Premium SMS Service"
                    ),
                    
                    # Send window: Schedule message delivery
                    send_window=SendWindow(
                        start_date="2026-03-21",  # YYYY-MM-DD
                        start_time="09:00:00",    # HH:MM:SS
                        stop_date="2026-03-21",   # Optional
                        stop_time="17:00:00"      # Optional
                    ),
                    
                    # Custom parameters
                    parameter=[
                        Parameter(key="campaign_id", value="spring2026"),
                        Parameter(key="segment", value="premium"),
                        Parameter(key="custom_field", value="custom_value")
                    ]
                )
            )
        ]
    )
    
    # Send message
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        print(f"✓ Advanced SMS sent successfully!")
        print(f"Batch Reference: {response.batch_reference}")
        
        for status in response.message_status:
            print(f"\nMessage Details:")
            print(f"  Message ID: {status.message_id}")
            print(f"  Recipient: {status.recipient}")
            print(f"  Status Code: {status.status_code}")
            print(f"  Status Message: {status.status_message}")
            print(f"  Client Reference: {status.client_reference}")
            print(f"  Sequence Index: {status.sequence_index}")
            
    except Exception as e:
        print(f"✗ Failed to send SMS: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(send_advanced_sms())
