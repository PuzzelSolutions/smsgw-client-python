"""Example of sending SMS to multiple recipients.

This example demonstrates:
- Sending the same message to multiple recipients
- Sending personalized messages to different recipients
- Batch sending with rate limiting
"""

import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message


async def send_to_multiple_recipients():
    """Send SMS to multiple recipients."""
    
    # Configuration - Replace with your actual values
    BASE_URL = "https://smsgw.puzzel.com"
    SERVICE_ID = 12345  # Your Puzzel service ID
    USERNAME = "your_username"  # Your Puzzel username
    PASSWORD = "your_password"  # Your Puzzel password
    
    # Setup client
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = BASE_URL
    
    client = MtHttpClient(request_adapter)
    
    print("=== Multiple Recipients Examples ===\n")
    
    # Example 1: Same message to multiple recipients
    print("1. Sending same message to multiple recipients...")
    
    recipients = [
        "+47xxxxxxxx1",
        "+47xxxxxxxx2",
        "+47xxxxxxxx3",
    ]
    
    messages = [
        Message(
            recipient=recipient,
            content="This is a bulk message sent to multiple recipients"
        )
        for recipient in recipients
    ]
    
    request = GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        batch_reference="bulk-message-batch",
        message=messages
    )
    
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        print(f"✓ Sent {len(response.message_status)} messages")
        print(f"Batch Reference: {response.batch_reference}\n")
        
        for status in response.message_status:
            print(f"  Recipient: {status.recipient}")
            print(f"  Message ID: {status.message_id}")
            print(f"  Status: {status.status_message}")
            print()
            
    except Exception as e:
        print(f"✗ Failed to send messages: {e}")
    
    print("="*50 + "\n")
    
    # Example 2: Personalized messages to different recipients
    print("2. Sending personalized messages...")
    
    personalized_data = [
        {
            "recipient": "+47xxxxxxxx1",
            "name": "Alice",
            "appointment_time": "10:00",
            "reference": "appt-alice-001"
        },
        {
            "recipient": "+47xxxxxxxx2",
            "name": "Bob",
            "appointment_time": "11:00",
            "reference": "appt-bob-002"
        },
        {
            "recipient": "+47xxxxxxxx3",
            "name": "Charlie",
            "appointment_time": "12:00",
            "reference": "appt-charlie-003"
        },
    ]
    
    personalized_messages = [
        Message(
            recipient=data["recipient"],
            content=f"Hello {data['name']}, your appointment is at {data['appointment_time']}",
            client_reference=data["reference"]
        )
        for data in personalized_data
    ]
    
    request = GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        batch_reference="personalized-batch",
        message=personalized_messages
    )
    
    try:
        response = await client.gw.rs.send_messages.post(request)
        
        print(f"✓ Sent {len(response.message_status)} personalized messages")
        print(f"Batch Reference: {response.batch_reference}\n")
        
        for status in response.message_status:
            print(f"  Recipient: {status.recipient}")
            print(f"  Reference: {status.client_reference}")
            print(f"  Status: {status.status_message}")
            print()
            
    except Exception as e:
        print(f"✗ Failed to send personalized messages: {e}")
    
    print("="*50 + "\n")
    
    # Example 3: Batch sending with rate limiting
    print("3. Batch sending with rate limiting...")
    print("⚠️  This example shows how to send large batches with rate limiting\n")
    
    # Simulate a large list of recipients
    large_recipient_list = [f"+4712345{i:04d}" for i in range(500)]
    
    batch_size = 100
    delay_between_batches = 2.0  # seconds
    total_sent = 0
    
    print(f"Sending to {len(large_recipient_list)} recipients in batches of {batch_size}")
    print(f"Delay between batches: {delay_between_batches} seconds\n")
    
    try:
        for i in range(0, len(large_recipient_list), batch_size):
            batch_recipients = large_recipient_list[i:i + batch_size]
            
            batch_messages = [
                Message(
                    recipient=recipient,
                    content="Rate-limited bulk message"
                )
                for recipient in batch_recipients
            ]
            
            request = GatewayRequest(
                service_id=SERVICE_ID,
                username=USERNAME,
                password=PASSWORD,
                batch_reference=f"rate-limited-batch-{i // batch_size}",
                message=batch_messages
            )
            
            # Uncomment to actually send:
            # response = await client.gw.rs.send_messages.post(request)
            # total_sent += len(response.message_status)
            
            # For demo purposes, just print what would happen:
            print(f"  Batch {i // batch_size + 1}: Would send {len(batch_messages)} messages")
            print(f"  Batch reference: rate-limited-batch-{i // batch_size}")
            
            # Wait before next batch (except for last batch)
            if i + batch_size < len(large_recipient_list):
                print(f"  Waiting {delay_between_batches} seconds...\n")
                await asyncio.sleep(delay_between_batches)
        
        print(f"\n✓ Would send {len(large_recipient_list)} messages in total")
        print("  (Uncomment the send line in the code to actually send)")
        
    except Exception as e:
        print(f"✗ Failed during batch sending: {e}")


if __name__ == "__main__":
    asyncio.run(send_to_multiple_recipients())
