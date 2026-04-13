# API Models Reference

This document provides detailed information about all the data models used in the Puzzel SMS Gateway Python Client.

## Table of Contents

- [Request Models](#request-models)
- [Response Models](#response-models)
- [Message Models](#message-models)
- [Settings Models](#settings-models)
- [Batch Models](#batch-models)
- [Error Models](#error-models)
- [Enums](#enums)

## Request Models

### GatewayRequest

The main request object for sending SMS messages.

**Location:** `src/models/gateway_request.py`

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `service_id` | `int` | No | Your service ID for the SMS Gateway |
| `username` | `str` | Yes | Authentication username |
| `password` | `str` | Yes | Authentication password |
| `batch_reference` | `str` | No | Optional reference for the batch of messages |
| `message` | `list[Message]` | Yes | List of messages to send |

**Example:**

```python
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

request = GatewayRequest(
    service_id=12345,
    username="your_username",
    password="your_password",
    batch_reference="batch-001",
    message=[
        Message(recipient="+47xxxxxxxxx", content="Hello World")
    ]
)
```

## Response Models

### GatewayResponse

Response received after sending messages.

**Location:** `src/models/gateway_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `batch_reference` | `str` | Reference ID for the batch of messages |
| `message_status` | `list[MessageStatus]` | Status information for each message sent |

**Example:**

```python
response = await client.gw.rs.send_messages.post(request)

print(f"Batch Reference: {response.batch_reference}")
for status in response.message_status:
    print(f"Message ID: {status.message_id}, Status: {status.status_message}")
```

### MessageStatus

Status information for an individual message.

**Location:** `src/models/message_status.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status_code` | `int` | Status code (1 = success, other values indicate errors) |
| `status_message` | `str` | Human-readable status message |
| `client_reference` | `str` | Client-provided reference for the message |
| `recipient` | `str` | Phone number of the recipient |
| `message_id` | `str` | Unique identifier for the message |
| `session_id` | `str` | Session identifier if applicable |
| `sequence_index` | `int` | Index of the message in the batch |

**Common Status Codes:**

- `1`: Message enqueued for sending (success)
- `2`: Message rejected (invalid recipient, content, etc.)
- `3`: Message failed (technical error)

**Example:**

```python
for status in response.message_status:
    if status.status_code == 1:
        print(f"✓ Message {status.message_id} sent to {status.recipient}")
    else:
        print(f"✗ Message failed: {status.status_message}")
```

## Message Models

### Message

Individual SMS message.

**Location:** `src/models/message.py`

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recipient` | `str` | Yes | Phone number with country code (e.g., +47xxxxxxxxx) |
| `content` | `str` | Yes | Message text content (max 1600 characters) |
| `price` | `int` | No | Price in cents/øre for premium SMS |
| `price_xml` | `str` | No | XML-formatted price information |
| `client_reference` | `str` | No | Your reference for tracking the message |
| `settings` | `Settings` | No | Additional message settings |

**Example:**

```python
from src.models.message import Message
from src.models.settings import Settings

message = Message(
    recipient="+47xxxxxxxxx",
    content="Hello World!",
    price=100,  # 1 NOK
    client_reference="msg-12345",
    settings=Settings(priority=1)
)
```

**Notes:**

- Phone numbers must include country code (e.g., +47 for Norway)
- Content length: Standard SMS = 160 chars, Unicode SMS = 70 chars
- Longer messages are automatically split into multiple SMS parts
- Use `auto_detect_encoding` in settings for automatic encoding detection

## Settings Models

### Settings

Message-level configuration options.

**Location:** `src/models/settings.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `priority` | `int` | Message priority (1=highest, 2=normal, 3=lowest) |
| `validity` | `int` | Validity period in minutes (how long to try delivery) |
| `differentiator` | `str` | Identifier for grouping messages |
| `invoice_node` | `str` | Invoice/cost center reference |
| `age` | `int` | Age restriction for content |
| `new_session` | `bool` | Start a new session |
| `session_id` | `str` | Session identifier |
| `auto_detect_encoding` | `bool` | Automatically detect and use optimal encoding |
| `originator_settings` | `OriginatorSettings` | Sender ID configuration |
| `gas_settings` | `GasSettings` | GAS (Gateway API Service) settings |
| `send_window` | `SendWindow` | Schedule message delivery |
| `parameter` | `list[Parameter]` | Custom key-value parameters |

**Example:**

```python
from src.models.settings import Settings

settings = Settings(
    priority=1,
    validity=173,
    differentiator="campaign-2026",
    invoice_node="marketing",
    age=18,
    auto_detect_encoding=True
)
```

### SendWindow

Schedule messages for delivery within a specific time window.

**Location:** `src/models/send_window.py`

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start_date` | `str` | Yes | Start date in format YYYY-MM-DD |
| `start_time` | `str` | Yes | Start time in format HH:MM:SS |
| `stop_date` | `str` | No | End date in format YYYY-MM-DD |
| `stop_time` | `str` | No | End time in format HH:MM:SS |

**Example:**

```python
from src.models.send_window import SendWindow

# Send tomorrow between 9 AM and 5 PM
send_window = SendWindow(
    start_date="2026-03-21",
    start_time="09:00:00",
    stop_date="2026-03-21",
    stop_time="17:00:00"
)
```

**Notes:**

- If `stop_date` is omitted, messages are sent as soon as possible after `start_date` and `start_time`
- Times are in the gateway server's timezone
- Messages outside the window are queued and sent when the window opens

### OriginatorSettings

Configure the sender ID (originator) for messages.

**Location:** `src/models/originator_settings.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `originator` | `str` | Sender ID (phone number, short code, or alphanumeric) |
| `originator_type` | `OriginatorType` | Type of originator |

**Example:**

```python
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

# Alphanumeric sender
originator = OriginatorSettings(
    originator="MyCompany",
    originator_type=OriginatorType.Alphanumeric
)

# Short code
originator = OriginatorSettings(
    originator="1960",
    originator_type=OriginatorType.Network
)

# International number
originator = OriginatorSettings(
    originator="+47xxxxxxxxx",
    originator_type=OriginatorType.International
)
```

**Notes:**

- Alphanumeric: Up to 11 characters (A-Z, a-z, 0-9)
- Network: Short codes (e.g., 1960)
- International: Full phone number with country code
- Not all originators are supported in all countries

### GasSettings

GAS (Gateway API Service) configuration for premium SMS.

**Location:** `src/models/gas_settings.py`

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `service_code` | `str` | Yes | Service code for billing |
| `description` | `str` | No | Description of the service |

**Example:**

```python
from src.models.gas_settings import GasSettings

gas_settings = GasSettings(
    service_code="02001",
    description="Premium SMS Service"
)
```

### Parameter

Custom key-value parameters for advanced use cases.

**Location:** `src/models/parameter.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `key` | `str` | Parameter name |
| `value` | `str` | Parameter value |

**Example:**

```python
from src.models.parameter import Parameter

parameters = [
    Parameter(key="campaign_id", value="spring2026"),
    Parameter(key="segment", value="premium"),
    Parameter(key="dcs", value="F5"),
    Parameter(key="pid", value="65")
]
```

**Common Parameters:**

- `business_model`: Business model identifier
- `dcs`: Data Coding Scheme
- `udh`: User Data Header
- `pid`: Protocol Identifier
- `flash`: Flash SMS indicator
- `parsing_type`: Content parsing type

## Batch Models

### BatchListResponse

List of message batches.

**Location:** `src/models/batch_list_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `message_batch` | `list[BatchResponse]` | List of batch information |

**Example:**

```python
batch_list = await client.management.by_service_id(service_id).batch.get()

for batch in batch_list.message_batch:
    print(f"Batch: {batch.client_batch_reference}")
    print(f"Total: {batch.total_size}, On Hold: {batch.on_hold}")
```

### BatchResponse

Information about a message batch.

**Location:** `src/models/batch_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `client_batch_reference` | `str` | Batch reference identifier |
| `total_size` | `int` | Total number of messages in batch |
| `on_hold` | `int` | Number of messages still pending |

**Example:**

```python
batch = batch_response.message_batch
print(f"Batch {batch.client_batch_reference}:")
print(f"  Total messages: {batch.total_size}")
print(f"  Pending: {batch.on_hold}")
print(f"  Sent: {batch.total_size - batch.on_hold}")
```

### BatchSingleResponse

Single batch details.

**Location:** `src/models/batch_single_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `message_batch` | `BatchResponse` | Batch information |

**Example:**

```python
batch_details = await client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_ref).get()

batch = batch_details.message_batch
print(f"Batch details: {batch.client_batch_reference}")
```

### StopBatchResponse

Response when stopping a batch.

**Location:** `src/models/stop_batch_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `service_id` | `int` | Service ID |
| `client_batch_reference` | `str` | Batch reference |
| `stopped_messages` | `list[StoppedMessageResponse]` | List of stopped messages |

**Example:**

```python
stop_response = await client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_ref).delete()

print(f"Stopped {len(stop_response.stopped_messages)} messages")
for msg in stop_response.stopped_messages:
    print(f"  Message ID: {msg.message_id}")
```

### StoppedMessageResponse

Information about a stopped message.

**Location:** `src/models/stopped_message_response.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | `str` | Gateway message ID |
| `client_message_reference` | `str` | Client-provided reference |

## Error Models

### ProblemDetails

Standard error response following RFC 7807.

**Location:** `src/models/problem_details.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | URI reference identifying the problem type |
| `title` | `str` | Short, human-readable summary |
| `status` | `int` | HTTP status code |
| `detail` | `str` | Detailed explanation |
| `instance` | `str` | URI reference to the specific occurrence |

**Example:**

```python
try:
    response = await client.gw.rs.send_messages.post(request)
except Exception as e:
    if hasattr(e, 'error') and isinstance(e.error, ProblemDetails):
        problem = e.error
        print(f"Error: {problem.title}")
        print(f"Status: {problem.status}")
        print(f"Detail: {problem.detail}")
```

**Common Error Scenarios:**

- `401 Unauthorized`: Invalid credentials
- `404 Not Found`: Batch reference not found
- `400 Bad Request`: Invalid request parameters

## Enums

### OriginatorType

Type of message originator/sender.

**Location:** `src/models/originator_type.py`

**Values:**

| Value | Description |
|-------|-------------|
| `International` | International phone number format (+country code) |
| `Alphanumeric` | Alphanumeric sender ID (up to 11 characters) |
| `Network` | Network-specific short code |

**Example:**

```python
from src.models.originator_type import OriginatorType

# Use in OriginatorSettings
originator_type = OriginatorType.Alphanumeric  # For "MyCompany"
originator_type = OriginatorType.Network       # For "1960"
originator_type = OriginatorType.International # For "+47xxxxxxxxx"
```

## Model Relationships

```
GatewayRequest
├── service_id: int
├── username: str
├── password: str
├── batch_reference: str
└── message: list[Message]
    ├── recipient: str
    ├── content: str
    ├── price: int
    ├── client_reference: str
    └── settings: Settings
        ├── priority: int
        ├── validity: int
        ├── originator_settings: OriginatorSettings
        │   ├── originator: str
        │   └── originator_type: OriginatorType
        ├── gas_settings: GasSettings
        │   ├── service_code: str
        │   └── description: str
        ├── send_window: SendWindow
        │   ├── start_date: str
        │   ├── start_time: str
        │   ├── stop_date: str
        │   └── stop_time: str
        └── parameter: list[Parameter]
            ├── key: str
            └── value: str

GatewayResponse
├── batch_reference: str
└── message_status: list[MessageStatus]
    ├── status_code: int
    ├── status_message: str
    ├── recipient: str
    ├── message_id: str
    └── sequence_index: int
```

## Type Hints and Validation

All models are Python dataclasses with type hints:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Message:
    recipient: Optional[str] = None
    content: Optional[str] = None
    price: Optional[int] = None
    # ... other fields
```

This provides:

- IDE autocomplete and type checking
- Runtime type validation (when using type checkers like mypy)
- Clear documentation of expected types
- Better error messages

## Serialization

Models use Kiota's serialization framework:

- **JSON**: Default format for requests and responses
- **XML**: Also supported (set appropriate headers)
- **Automatic**: Handled by the request adapter

You don't need to manually serialize/deserialize - the client handles this automatically:

```python
# Automatic serialization
request = GatewayRequest(...)  # Python object
response = await client.gw.rs.send_messages.post(request)  # Automatically serialized to JSON

# Automatic deserialization
print(response.batch_reference)  # Python object from JSON response
```

## Best Practices

1. **Use Type Hints**: Take advantage of the type hints for better IDE support
2. **Validate Input**: Validate phone numbers and content before creating messages
3. **Handle Optionals**: Check for `None` values in optional fields
4. **Reuse Objects**: Create reusable settings objects for common configurations
5. **Check Status Codes**: Always check `status_code` in `MessageStatus` responses

## Summary

This document covered:

- All request and response models
- Message and settings configuration
- Batch management models
- Error handling models
- Enums and type definitions
- Model relationships and structure

For usage examples, see:
- [Main README](../README.md) - Main documentation
- [04 - Examples](04-examples.md) - Code examples
- [06 - Advanced](06-advanced.md) - Advanced topics
