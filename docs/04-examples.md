# Usage Examples

This document provides comprehensive examples for using the Puzzel SMS Gateway Python Client (Kiota).

## Table of Contents

- [Setup and Configuration](#setup-and-configuration)
- [Basic Examples](#basic-examples)
- [Message Settings](#message-settings)
- [Batch Operations](#batch-operations)
- [Advanced Use Cases](#advanced-use-cases)
- [Error Handling](#error-handling)
- [Production Patterns](#production-patterns)

## Setup and Configuration

### Basic Client Setup

```python
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient

def create_client(base_url: str) -> MtHttpClient:
    """Create and configure the SMS Gateway client."""
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url
    return MtHttpClient(request_adapter)

# Usage
client = create_client("https://your-gateway-server.com")
```

### Configuration with Environment Variables

```python
import os
from typing import Optional

class SmsConfig:
    """Configuration for SMS Gateway client."""
    
    def __init__(self):
        self.base_url = os.getenv("SMS_GATEWAY_BASE_URL", "https://your-gateway-server.com")
        self.service_id = int(os.getenv("SMS_GATEWAY_SERVICE_ID", "0"))
        self.username = os.getenv("SMS_GATEWAY_USERNAME", "")
        self.password = os.getenv("SMS_GATEWAY_PASSWORD", "")
    
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        return all([
            self.base_url,
            self.service_id > 0,
            self.username,
            self.password
        ])

# Usage
config = SmsConfig()
if not config.validate():
    raise ValueError("Missing required SMS Gateway configuration")

client = create_client(config.base_url)
```

## Basic Examples

### Send a Single SMS

```python
import asyncio
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

async def send_single_sms(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send a single SMS message."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[
            Message(
                recipient=recipient,
                content=content
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    
    print(f"Batch Reference: {response.batch_reference}")
    for status in response.message_status:
        print(f"Recipient: {status.recipient}")
        print(f"Message ID: {status.message_id}")
        print(f"Status Code: {status.status_code}")
        print(f"Status Message: {status.status_message}")
    
    return response

# Run
asyncio.run(send_single_sms(
    client,
    config,
    "+47xxxxxxxxx",
    "Hello from Puzzel SMS Gateway!"
))
```

### Send Multiple SMS Messages

```python
async def send_multiple_sms(
    client: MtHttpClient,
    config: SmsConfig,
    recipients: list[str],
    content: str
):
    """Send the same message to multiple recipients."""
    messages = [
        Message(recipient=recipient, content=content)
        for recipient in recipients
    ]
    
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=messages
    )
    
    response = await client.gw.rs.send_messages.post(request)
    
    print(f"Sent {len(response.message_status)} messages")
    print(f"Batch Reference: {response.batch_reference}")
    
    return response

# Run
recipients = ["+47xxxxxxxx1", "+47xxxxxxxx2", "+47xxxxxxxx3"]
asyncio.run(send_multiple_sms(client, config, recipients, "Bulk message"))
```

### Send Personalized Messages

```python
async def send_personalized_messages(
    client: MtHttpClient,
    config: SmsConfig,
    messages_data: list[dict]
):
    """Send personalized messages to different recipients."""
    messages = [
        Message(
            recipient=data["recipient"],
            content=data["content"],
            client_reference=data.get("reference")
        )
        for data in messages_data
    ]
    
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        batch_reference="personalized-batch-001",
        message=messages
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run
messages_data = [
    {
        "recipient": "+47xxxxxxxx1",
        "content": "Hello Alice, your appointment is at 10:00",
        "reference": "appt-alice-001"
    },
    {
        "recipient": "+47xxxxxxxx2",
        "content": "Hello Bob, your appointment is at 11:00",
        "reference": "appt-bob-002"
    }
]
asyncio.run(send_personalized_messages(client, config, messages_data))
```

## Message Settings

### Scheduled Messages with Send Window

```python
from src.models.settings import Settings
from src.models.send_window import SendWindow
from datetime import datetime, timedelta

async def send_scheduled_message(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str,
    send_date: str,
    start_time: str,
    end_time: str
):
    """Send a message within a specific time window."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[
            Message(
                recipient=recipient,
                content=content,
                settings=Settings(
                    send_window=SendWindow(
                        start_date=send_date,
                        start_time=start_time,
                        stop_date=send_date,
                        stop_time=end_time
                    )
                )
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run - schedule for tomorrow between 9 AM and 5 PM
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
asyncio.run(send_scheduled_message(
    client,
    config,
    "+47xxxxxxxxx",
    "Scheduled reminder",
    tomorrow,
    "09:00:00",
    "17:00:00"
))
```

### Custom Originator

```python
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

async def send_with_custom_originator(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str,
    originator: str,
    originator_type: OriginatorType
):
    """Send a message with a custom sender ID."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[
            Message(
                recipient=recipient,
                content=content,
                settings=Settings(
                    originator_settings=OriginatorSettings(
                        originator=originator,
                        originator_type=originator_type
                    )
                )
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run with alphanumeric sender
asyncio.run(send_with_custom_originator(
    client,
    config,
    "+47xxxxxxxxx",
    "Message from MyCompany",
    "MyCompany",
    OriginatorType.Alphanumeric
))

# Run with short code
asyncio.run(send_with_custom_originator(
    client,
    config,
    "+47xxxxxxxxx",
    "Message from short code",
    "1960",
    OriginatorType.Network
))
```

### Priority and Validity

```python
async def send_with_priority(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str,
    priority: int = 1,
    validity_minutes: int = 173
):
    """Send a message with priority and validity settings."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[
            Message(
                recipient=recipient,
                content=content,
                settings=Settings(
                    priority=priority,  # 1 = highest, 3 = lowest
                    validity=validity_minutes  # How long to try delivery
                )
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run with high priority and short validity
asyncio.run(send_with_priority(
    client,
    config,
    "+47xxxxxxxxx",
    "Urgent: Time-sensitive message",
    priority=1,
    validity_minutes=60
))
```

### Premium SMS with GAS Settings

```python
from src.models.gas_settings import GasSettings

async def send_premium_sms(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str,
    price: int,
    service_code: str
):
    """Send a premium SMS with pricing."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[
            Message(
                recipient=recipient,
                content=content,
                price=price,  # Price in cents/øre
                settings=Settings(
                    gas_settings=GasSettings(
                        service_code=service_code,
                        description="Premium SMS Service"
                    )
                )
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run
asyncio.run(send_premium_sms(
    client,
    config,
    "+47xxxxxxxxx",
    "Premium content message",
    price=100,  # 1 NOK
    service_code="02001"
))
```

### Complete Message Configuration

```python
from src.models.parameter import Parameter

async def send_fully_configured_message(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send a message with all available configuration options."""
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        batch_reference="campaign-spring-2026",
        message=[
            Message(
                recipient=recipient,
                content=content,
                price=100,
                client_reference="msg-ref-12345",
                settings=Settings(
                    priority=1,
                    validity=173,
                    differentiator="marketing-campaign",
                    invoice_node="marketing-department",
                    age=18,
                    new_session=True,
                    session_id="session-abc123",
                    auto_detect_encoding=True,
                    originator_settings=OriginatorSettings(
                        originator="MyBrand",
                        originator_type=OriginatorType.Alphanumeric
                    ),
                    gas_settings=GasSettings(
                        service_code="02001",
                        description="Marketing SMS"
                    ),
                    send_window=SendWindow(
                        start_date="2026-03-21",
                        start_time="09:00:00",
                        stop_date="2026-03-21",
                        stop_time="17:00:00"
                    ),
                    parameter=[
                        Parameter(key="campaign_id", value="spring2026"),
                        Parameter(key="segment", value="premium")
                    ]
                )
            )
        ]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run
asyncio.run(send_fully_configured_message(
    client,
    config,
    "+47xxxxxxxxx",
    "Complete configuration example"
))
```

## Batch Operations

### List All Batches

```python
async def list_all_batches(client: MtHttpClient, service_id: int):
    """List all message batches for a service."""
    batch_list = await client.management.by_service_id(service_id).batch.get()
    
    print(f"Total batches: {len(batch_list.message_batch)}")
    for batch in batch_list.message_batch:
        print(f"\nBatch Reference: {batch.client_batch_reference}")
        print(f"Total Messages: {batch.total_size}")
        print(f"Messages On Hold: {batch.on_hold}")
    
    return batch_list

# Run
asyncio.run(list_all_batches(client, config.service_id))
```

### Get Batch Details

```python
async def get_batch_details(
    client: MtHttpClient,
    service_id: int,
    batch_reference: str
):
    """Get details of a specific batch."""
    batch_details = await client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_reference).get()
    
    batch = batch_details.message_batch
    print(f"Batch Reference: {batch.client_batch_reference}")
    print(f"Total Size: {batch.total_size}")
    print(f"On Hold: {batch.on_hold}")
    
    return batch_details

# Run
asyncio.run(get_batch_details(client, config.service_id, "my-batch-reference"))
```

### Stop a Batch

```python
async def stop_batch(
    client: MtHttpClient,
    service_id: int,
    batch_reference: str
):
    """Stop all pending messages in a batch."""
    stop_response = await client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_reference).delete()
    
    print(f"Service ID: {stop_response.service_id}")
    print(f"Batch Reference: {stop_response.client_batch_reference}")
    print(f"Stopped Messages: {len(stop_response.stopped_messages)}")
    
    for stopped in stop_response.stopped_messages:
        print(f"  Message ID: {stopped.message_id}")
        print(f"  Client Reference: {stopped.client_message_reference}")
    
    return stop_response

# Run
asyncio.run(stop_batch(client, config.service_id, "my-batch-reference"))
```

### Monitor Batch Status

```python
import asyncio

async def monitor_batch_until_complete(
    client: MtHttpClient,
    service_id: int,
    batch_reference: str,
    check_interval: int = 5
):
    """Monitor a batch until all messages are sent."""
    while True:
        batch_details = await client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_reference).get()
        batch = batch_details.message_batch
        
        print(f"Batch: {batch.client_batch_reference}")
        print(f"Total: {batch.total_size}, On Hold: {batch.on_hold}")
        
        if batch.on_hold == 0:
            print("All messages sent!")
            break
        
        print(f"Waiting {check_interval} seconds before next check...")
        await asyncio.sleep(check_interval)

# Run
asyncio.run(monitor_batch_until_complete(client, config.service_id, "my-batch-reference"))
```

## Advanced Use Cases

### Retry Logic with Exponential Backoff

```python
import asyncio
from typing import Optional

async def send_with_retry(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str,
    max_retries: int = 3,
    initial_delay: float = 1.0
):
    """Send SMS with exponential backoff retry logic."""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            request = GatewayRequest(
                service_id=config.service_id,
                username=config.username,
                password=config.password,
                message=[Message(recipient=recipient, content=content)]
            )
            
            response = await client.gw.rs.send_messages.post(request)
            print(f"Success on attempt {attempt + 1}")
            return response
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print("Max retries reached")
                raise

# Run
asyncio.run(send_with_retry(client, config, "+47xxxxxxxxx", "Retry example"))
```

### Batch Processing with Rate Limiting

```python
import asyncio
from typing import List

async def send_batch_with_rate_limit(
    client: MtHttpClient,
    config: SmsConfig,
    recipients: List[str],
    content: str,
    batch_size: int = 100,
    delay_between_batches: float = 1.0
):
    """Send messages in batches with rate limiting."""
    total_sent = 0
    
    for i in range(0, len(recipients), batch_size):
        batch_recipients = recipients[i:i + batch_size]
        
        messages = [
            Message(recipient=recipient, content=content)
            for recipient in batch_recipients
        ]
        
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            batch_reference=f"rate-limited-batch-{i // batch_size}",
            message=messages
        )
        
        response = await client.gw.rs.send_messages.post(request)
        total_sent += len(response.message_status)
        
        print(f"Sent batch {i // batch_size + 1}: {len(response.message_status)} messages")
        print(f"Total sent: {total_sent}/{len(recipients)}")
        
        if i + batch_size < len(recipients):
            await asyncio.sleep(delay_between_batches)
    
    return total_sent

# Run
large_recipient_list = [f"+4712345{i:04d}" for i in range(500)]
asyncio.run(send_batch_with_rate_limit(
    client,
    config,
    large_recipient_list,
    "Bulk message",
    batch_size=100,
    delay_between_batches=2.0
))
```

### Concurrent Message Sending

```python
import asyncio
from typing import List, Tuple

async def send_concurrent_messages(
    client: MtHttpClient,
    config: SmsConfig,
    messages_data: List[Tuple[str, str]]
):
    """Send multiple messages concurrently."""
    
    async def send_single(recipient: str, content: str):
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            message=[Message(recipient=recipient, content=content)]
        )
        return await client.gw.rs.send_messages.post(request)
    
    tasks = [send_single(recipient, content) for recipient, content in messages_data]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = sum(1 for r in responses if not isinstance(r, Exception))
    failed = len(responses) - successful
    
    print(f"Successful: {successful}, Failed: {failed}")
    
    return responses

# Run
messages = [
    ("+47xxxxxxxx1", "Message 1"),
    ("+47xxxxxxxx2", "Message 2"),
    ("+47xxxxxxxx3", "Message 3"),
]
asyncio.run(send_concurrent_messages(client, config, messages))
```

## Error Handling

### Comprehensive Error Handling

```python
from src.models.problem_details import ProblemDetails

async def send_with_comprehensive_error_handling(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send SMS with comprehensive error handling."""
    try:
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            message=[Message(recipient=recipient, content=content)]
        )
        
        response = await client.gw.rs.send_messages.post(request)
        
        # Check individual message statuses
        for status in response.message_status:
            if status.status_code != 1:  # 1 = success
                print(f"Warning: Message to {status.recipient} has status {status.status_code}: {status.status_message}")
        
        return response
        
    except Exception as e:
        # Check if it's an API error with ProblemDetails
        if hasattr(e, 'error') and isinstance(e.error, ProblemDetails):
            problem = e.error
            print(f"API Error: {problem.title}")
            print(f"Status Code: {problem.status}")
            print(f"Detail: {problem.detail}")
            print(f"Type: {problem.type}")
            print(f"Instance: {problem.instance}")
        else:
            print(f"Unexpected error: {type(e).__name__}: {e}")
        
        raise

# Run
asyncio.run(send_with_comprehensive_error_handling(
    client,
    config,
    "+47xxxxxxxxx",
    "Error handling example"
))
```

### Validation Before Sending

```python
import re

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, phone))

def validate_message_content(content: str) -> bool:
    """Validate message content."""
    return 0 < len(content) <= 1600  # SMS length limit

async def send_with_validation(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send SMS with input validation."""
    # Validate inputs
    if not validate_phone_number(recipient):
        raise ValueError(f"Invalid phone number format: {recipient}")
    
    if not validate_message_content(content):
        raise ValueError(f"Invalid message content length: {len(content)}")
    
    # Send if validation passes
    request = GatewayRequest(
        service_id=config.service_id,
        username=config.username,
        password=config.password,
        message=[Message(recipient=recipient, content=content)]
    )
    
    response = await client.gw.rs.send_messages.post(request)
    return response

# Run
asyncio.run(send_with_validation(client, config, "+47xxxxxxxxx", "Validated message"))
```

## Production Patterns

### Context Manager for Client

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def sms_client(base_url: str):
    """Context manager for SMS client lifecycle."""
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = base_url
    client = MtHttpClient(request_adapter)
    
    try:
        yield client
    finally:
        # Cleanup if needed
        pass

# Usage
async def main():
    async with sms_client("https://your-gateway-server.com") as client:
        request = GatewayRequest(
            service_id=12345,
            username="user",
            password="pass",
            message=[Message(recipient="+47xxxxxxxxx", content="Hello")]
        )
        response = await client.gw.rs.send_messages.post(request)
        print(f"Sent: {response.batch_reference}")

asyncio.run(main())
```

### Logging Integration

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_with_logging(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send SMS with comprehensive logging."""
    logger.info(f"Preparing to send SMS to {recipient}")
    
    try:
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            message=[Message(recipient=recipient, content=content)]
        )
        
        logger.debug(f"Request: service_id={config.service_id}, recipients=1")
        
        response = await client.gw.rs.send_messages.post(request)
        
        logger.info(f"SMS sent successfully. Batch: {response.batch_reference}")
        
        for status in response.message_status:
            logger.info(
                f"Message {status.message_id}: "
                f"status={status.status_code}, "
                f"recipient={status.recipient}"
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}", exc_info=True)
        raise

# Run
asyncio.run(send_with_logging(client, config, "+47xxxxxxxxx", "Logged message"))
```

### Metrics and Monitoring

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class SmsMetrics:
    """Track SMS sending metrics."""
    total_sent: int = 0
    total_failed: int = 0
    batches_created: int = 0
    last_send_time: datetime = None
    
    def record_success(self, count: int = 1):
        self.total_sent += count
        self.last_send_time = datetime.now()
    
    def record_failure(self, count: int = 1):
        self.total_failed += count
    
    def record_batch(self):
        self.batches_created += 1
    
    def get_summary(self) -> Dict:
        return {
            "total_sent": self.total_sent,
            "total_failed": self.total_failed,
            "batches_created": self.batches_created,
            "success_rate": self.total_sent / (self.total_sent + self.total_failed) if (self.total_sent + self.total_failed) > 0 else 0,
            "last_send_time": self.last_send_time.isoformat() if self.last_send_time else None
        }

metrics = SmsMetrics()

async def send_with_metrics(
    client: MtHttpClient,
    config: SmsConfig,
    recipient: str,
    content: str
):
    """Send SMS with metrics tracking."""
    try:
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            message=[Message(recipient=recipient, content=content)]
        )
        
        response = await client.gw.rs.send_messages.post(request)
        
        metrics.record_success(len(response.message_status))
        metrics.record_batch()
        
        return response
        
    except Exception as e:
        metrics.record_failure()
        raise

# Run and check metrics
asyncio.run(send_with_metrics(client, config, "+47xxxxxxxxx", "Metrics example"))
print(metrics.get_summary())
```

## Summary

This document covered:

- Basic client setup and configuration
- Simple and advanced message sending
- Message settings and customization
- Batch management operations
- Error handling patterns
- Production-ready code patterns

For more information, see:
- [Main README](../README.md) - Main documentation
- [05 - Models](05-models.md) - API models reference
- [06 - Advanced](06-advanced.md) - Advanced topics and best practices
