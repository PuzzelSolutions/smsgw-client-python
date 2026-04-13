# Quick Reference Guide

A quick reference for common operations with the Puzzel SMS Gateway Python Client.

## Installation

```bash
# Install from PyPI
pip install puzzel-sms-gateway-client

# Or using uv (recommended)
uv pip install puzzel-sms-gateway-client
```

## Basic Setup

```python
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient

# Create client
auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = "https://your-gateway-server.com"
client = MtHttpClient(request_adapter)
```

## Send Simple SMS

```python
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

request = GatewayRequest(
    service_id=12345,
    username="your_username",
    password="your_password",
    message=[Message(recipient="+47xxxxxxxxx", content="Hello World")]
)

response = await client.gw.rs.send_messages.post(request)
print(f"Batch: {response.batch_reference}")
```

## Send to Multiple Recipients

```python
messages = [
    Message(recipient="+47xxxxxxxx1", content="Message 1"),
    Message(recipient="+47xxxxxxxx2", content="Message 2"),
]

request = GatewayRequest(
    service_id=12345,
    username="user",
    password="pass",
    message=messages
)

response = await client.gw.rs.send_messages.post(request)
```

## Schedule Message

```python
from src.models.settings import Settings
from src.models.send_window import SendWindow

message = Message(
    recipient="+47xxxxxxxxx",
    content="Scheduled message",
    settings=Settings(
        send_window=SendWindow(
            start_date="2026-03-21",
            start_time="09:00:00",
            stop_date="2026-03-21",
            stop_time="17:00:00"
        )
    )
)
```

## Custom Sender ID

```python
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

message = Message(
    recipient="+47xxxxxxxxx",
    content="Message with custom sender",
    settings=Settings(
        originator_settings=OriginatorSettings(
            originator="MyCompany",
            originator_type=OriginatorType.Alphanumeric
        )
    )
)
```

## Set Priority and Validity

```python
message = Message(
    recipient="+47xxxxxxxxx",
    content="High priority message",
    settings=Settings(
        priority=1,      # 1=highest, 2=normal, 3=lowest
        validity=60      # Minutes to try delivery
    )
)
```

## Premium SMS

```python
from src.models.gas_settings import GasSettings

message = Message(
    recipient="+47xxxxxxxxx",
    content="Premium content",
    price=100,  # Price in cents/øre
    settings=Settings(
        gas_settings=GasSettings(
            service_code="02001",
            description="Premium SMS"
        )
    )
)
```

## List All Batches

```python
batch_list = await client.management.by_service_id(12345).batch.get()

for batch in batch_list.message_batch:
    print(f"Batch: {batch.client_batch_reference}")
    print(f"Total: {batch.total_size}, Pending: {batch.on_hold}")
```

## Get Batch Details

```python
batch_details = await client.management.by_service_id(12345).batch.by_client_batch_reference("batch-ref").get()

batch = batch_details.message_batch
print(f"Total: {batch.total_size}, On Hold: {batch.on_hold}")
```

## Stop a Batch

```python
stop_response = await client.management.by_service_id(12345).batch.by_client_batch_reference("batch-ref").delete()

print(f"Stopped {len(stop_response.stopped_messages)} messages")
```

## Error Handling

```python
from src.models.problem_details import ProblemDetails

try:
    response = await client.gw.rs.send_messages.post(request)
except Exception as e:
    if hasattr(e, 'error') and isinstance(e.error, ProblemDetails):
        print(f"Error: {e.error.title} ({e.error.status})")
        print(f"Detail: {e.error.detail}")
    else:
        print(f"Error: {e}")
```

## Configuration with Environment Variables

```python
import os

config = {
    "base_url": os.getenv("SMS_GATEWAY_URL"),
    "service_id": int(os.getenv("SMS_SERVICE_ID")),
    "username": os.getenv("SMS_USERNAME"),
    "password": os.getenv("SMS_PASSWORD")
}
```

## Timeout Configuration

```python
import httpx

timeout = httpx.Timeout(30.0, connect=10.0)
http_client = httpx.AsyncClient(timeout=timeout)

request_adapter = HttpxRequestAdapter(auth_provider, http_client=http_client)
```

## Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def send_with_retry(client, request):
    return await client.gw.rs.send_messages.post(request)
```

## Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Sending SMS to {recipient}")
response = await client.gw.rs.send_messages.post(request)
logger.info(f"SMS sent: {response.batch_reference}")
```

## Common Status Codes

| Code | Meaning |
|------|---------|
| 1 | Message enqueued for sending (success) |
| 2 | Message rejected (invalid recipient, content, etc.) |
| 3 | Message failed (technical error) |

## Common Originator Types

| Type | Description | Example |
|------|-------------|---------|
| `OriginatorType.Alphanumeric` | Text sender ID (max 11 chars) | "MyCompany" |
| `OriginatorType.Network` | Short code | "1960" |
| `OriginatorType.International` | Phone number with country code | "+47xxxxxxxxx" |

## API Endpoints

| Endpoint                        | Purpose          |
|---------------------------------|------------------|
| `client.gw.rs.send_messages`  | Send messages    |
| `client.management`             | Batch management |

## Model Hierarchy

```
GatewayRequest
├── service_id
├── username
├── password
├── batch_reference
└── message: list[Message]
    ├── recipient
    ├── content
    ├── price
    ├── client_reference
    └── settings: Settings
        ├── priority
        ├── validity
        ├── originator_settings: OriginatorSettings
        ├── gas_settings: GasSettings
        ├── send_window: SendWindow
        └── parameter: list[Parameter]
```

## Phone Number Format

- Must include country code
- Format: `+[country code][number]`
- Example: `+47xxxxxxxxx` (Norway)
- Example: `+46xxxxxxxxx` (Sweden)
- Example: `+45xxxxxxxx` (Denmark)

## Message Length Limits

- Standard SMS (GSM-7): 160 characters
- Unicode SMS: 70 characters
- Longer messages are automatically split
- Maximum total length: 1600 characters

## Best Practices

1. **Always use async/await** - The client is fully asynchronous
2. **Validate phone numbers** - Check format before sending
3. **Handle errors** - Always wrap API calls in try/except
4. **Use batch references** - Track your message batches
5. **Check status codes** - Verify message status in responses
6. **Store credentials securely** - Use environment variables or secure storage
7. **Rate limit** - Implement delays for large batches
8. **Log operations** - Keep track of sent messages

## See Also

- [Main README](../README.md) - Main documentation
- [04 - Examples](04-examples.md) - Detailed examples
- [05 - Models](05-models.md) - Model reference
- [06 - Advanced](06-advanced.md) - Advanced topics
