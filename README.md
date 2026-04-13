# Puzzel SMS Gateway Python Client <!-- omit in toc -->

[![GitHub License](https://img.shields.io/github/license/PuzzelSolutions/smsgw-client-python?color=blue)](LICENSE)
[![Latest Version](https://img.shields.io/pypi/v/puzzel_sms_gateway_client.svg)](https://pypi.org/project/puzzel_sms_gateway_client/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/puzzel_sms_gateway_client.svg)](https://pypi.python.org/pypi/smsgw-client-python/)
[![Downloads](https://pepy.tech/badge/puzzel_sms_gateway_client)](https://pepy.tech/project/puzzel_sms_gateway_client)
[![Coverage](https://img.shields.io/codecov/c/github/PuzzelSolutions/smsgw-client-python?color=blue)](https://app.codecov.io/gh/PuzzelSolutions/smsgw-client-python)
[![GitHub issues](https://img.shields.io/github/issues-raw/PuzzelSolutions/smsgw-client-python)](https://github.com/PuzzelSolutions/smsgw-client-python/issues)
![GitHub last commit](https://img.shields.io/github/last-commit/PuzzelSolutions/smsgw-client-python)

Copyright 2024-2026 [Puzzel AS](https://www.puzzel.com)

## Contents

- [Contents](#contents)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
- [Installation](#installation)
  - [Using uv (Recommended)](#using-uv-recommended)
    - [Option 1: Install into Existing Project](#option-1-install-into-existing-project)
    - [Option 2: Create New Project with uv](#option-2-create-new-project-with-uv)
  - [Using pip](#using-pip)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
  - [Base URL Configuration](#base-url-configuration)
- [Usage Examples](#usage-examples)
  - [Basic Message Sending](#basic-message-sending)
  - [Sending with Message Settings](#sending-with-message-settings)
  - [Advanced Configuration](#advanced-configuration)
  - [Batch Management](#batch-management)
- [API Reference](#api-reference)
  - [Main Client](#main-client)
  - [API Endpoints](#api-endpoints)
  - [Models](#models)
  - [Request Builders](#request-builders)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Migration from v2.x](#migration-from-v2x)
  - [1. Async/Await Required](#1-asyncawait-required)
  - [2. Client Initialization](#2-client-initialization)
  - [3. Credentials in Request](#3-credentials-in-request)
  - [4. Model Structure](#4-model-structure)
  - [5. Fluent API](#5-fluent-api)
- [Publishing](#publishing)
- [Additional Documentation](#additional-documentation)
- [Support](#support)
- [License](#license)

## Overview

This is a Python client for the Puzzel SMS Gateway API. It provides a type-safe, fluent interface for sending SMS messages and managing message batches.

The client is generated from the SMS Gateway OpenAPI specification and uses the Kiota abstractions for HTTP communication, serialization, and authentication.

## Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Dependencies

The package automatically installs all required dependencies when you install it from PyPI:

- `microsoft-kiota-abstractions>=1.0.0` - Core Kiota abstractions
- `microsoft-kiota-http>=1.0.0` - HTTP request handling
- `microsoft-kiota-serialization-json>=1.0.0` - JSON serialization
- `microsoft-kiota-serialization-text>=1.0.0` - Text serialization
- `microsoft-kiota-serialization-form>=1.0.0` - Form serialization
- `microsoft-kiota-serialization-multipart>=1.0.0` - Multipart serialization
- `httpx>=0.24.0` - Async HTTP client

You don't need to install these manually - they're included automatically. See `pyproject.toml` for the complete list.

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

#### Option 1: Install into Existing Project

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Install the SMS Gateway client from PyPI
uv pip install puzzel-sms-gateway-client
```

#### Option 2: Create New Project with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Create a new project
uv init <projectname> --app --python 3.13.1
cd <projectname>

# Create virtual environment
uv venv --python 3.13.1 --seed
```

```bash
# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
```

```bash
# or
.venv\Scripts\activate     # On Windows
```

```bash
# Verify installation
python -V
uv pip list

# Install the SMS Gateway client from PyPI
uv pip install puzzel-sms-gateway-client
```

> **Note:** `uv init` typically creates `.venv/` automatically, but you can use `--seed` to explicitly ensure that pip, setuptools, and wheel are installed.

### Using pip

```bash
pip install puzzel-sms-gateway-client
```

## Quick Start

```python
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

async def send_sms():
    # Set up authentication and HTTP adapter
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://smsgw.puzzel.com"

    # Create the client
    client = MtHttpClient(request_adapter)

    # Create a message
    gateway_request = GatewayRequest(
        service_id=YOUR_SERVICE_ID,  # Your Puzzel service ID
        username="YOUR_USERNAME",     # Your Puzzel username
        password="YOUR_PASSWORD",     # Your Puzzel password
        message=[
            Message(
                recipient="+47xxxxxxxxx",  # Phone number with country code
                content="Hello World!"
            )
        ]
    )

    # Send the message
    response = await client.gw.rs.send_messages.post(gateway_request)

    print(f"Batch Reference: {response.batch_reference}")
    for status in response.message_status:
        print(f"Message ID: {status.message_id}")
        print(f"Status: {status.status_message}")

# Run the async function
asyncio.run(send_sms())
```

## Authentication

The SMS Gateway uses Basic Authentication passed through the request body. You need to provide:

- `service_id`: Your service ID (integer)
- `username`: Your gateway username (string)
- `password`: Your gateway password (string)

These credentials are included in the `GatewayRequest` object for each API call.

### Base URL Configuration

The Puzzel SMS Gateway base URL is: `https://smsgw.puzzel.com`

**Important**: Set only the base domain, not including any path:

```python
# ✅ Correct
request_adapter.base_url = "https://smsgw.puzzel.com"

# ❌ Wrong - don't include the path
request_adapter.base_url = "https://smsgw.puzzel.com/gw/rs"
```

The client automatically constructs the full URL path based on the API method you call.

```python
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

# Use AnonymousAuthenticationProvider since credentials are in the request body
auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = "https://smsgw.puzzel.com"
```

## Usage Examples

### Basic Message Sending

Send a simple SMS to a single recipient:

```python
import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message

async def send_basic_sms():
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://smsgw.puzzel.com"

    client = MtHttpClient(request_adapter)

    request = GatewayRequest(
        service_id=12345,
        username="your_username",
        password="your_password",
        message=[
            Message(
                recipient="+47xxxxxxxxx",
                content="Hello from Puzzel SMS Gateway!"
            )
        ]
    )

    response = await client.gw.rs.send_messages.post(request)
    return response

asyncio.run(send_basic_sms())
```

### Sending with Message Settings

Send an SMS with advanced settings like send window, originator, and priority:

```python
import asyncio
from src.mt_http_client import MtHttpClient
from src.models.gateway_request import GatewayRequest
from src.models.message import Message
from src.models.settings import Settings
from src.models.send_window import SendWindow
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

async def send_scheduled_sms():
    from kiota_abstractions.authentication import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter
    from src.mt_http_client import MtHttpClient

    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://smsgw.puzzel.com"

    client = MtHttpClient(request_adapter)

    request = GatewayRequest(
        service_id=12345,
        username="your_username",
        password="your_password",
        message=[
            Message(
                recipient="+47xxxxxxxxx",
                content="Scheduled message",
                settings=Settings(
                    priority=1,
                    validity=173,
                    originator_settings=OriginatorSettings(
                        originator="1960",
                        originator_type=OriginatorType.Network
                    ),
                    send_window=SendWindow(
                        start_date="2026-03-21",
                        start_time="09:00:00",
                        stop_date="2026-03-21",
                        stop_time="17:00:00"
                    )
                )
            )
        ]
    )

    response = await client.gw.rs.send_messages.post(request)
    return response

asyncio.run(send_scheduled_sms())
```

### Advanced Configuration

Send an SMS with all available options:

```python
import asyncio
from src.models.gateway_request import GatewayRequest
from src.models.message import Message
from src.models.settings import Settings
from src.models.gas_settings import GasSettings
from src.models.parameter import Parameter

async def send_advanced_sms():
    from kiota_abstractions.authentication import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter
    from src.mt_http_client import MtHttpClient

    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://smsgw.puzzel.com"

    client = MtHttpClient(request_adapter)

    request = GatewayRequest(
        service_id=12345,
        username="your_username",
        password="your_password",
        batch_reference="my-batch-001",
        message=[
            Message(
                recipient="+47xxxxxxxxx",
                content="Advanced message",
                price=100,
                client_reference="msg-ref-001",
                settings=Settings(
                    priority=1,
                    validity=173,
                    differentiator="campaign-spring-2026",
                    invoice_node="marketing-dept",
                    age=18,
                    new_session=True,
                    session_id="session-12345",
                    auto_detect_encoding=True,
                    gas_settings=GasSettings(
                        service_code="02001",
                        description="Premium SMS"
                    ),
                    parameter=[
                        Parameter(key="custom_key", value="custom_value")
                    ]
                )
            )
        ]
    )

    response = await client.gw.rs.send_messages.post(request)
    return response

asyncio.run(send_advanced_sms())
```

### Batch Management

List, retrieve, and stop message batches:

```python
import asyncio

async def manage_batches():
    from kiota_abstractions.authentication import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter
    from src.mt_http_client import MtHttpClient

    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://smsgw.puzzel.com"

    client = MtHttpClient(request_adapter)

    service_id = 12345
    batch_reference = "my-batch-001"

    # List all batches for a service
    batch_list = await client.mgmt.rs.service.by_service_id(service_id).batch.get()
    print(f"Total batches: {len(batch_list.message_batch)}")
    for batch in batch_list.message_batch:
        print(f"Batch: {batch.client_batch_reference}, Total: {batch.total_size}, On Hold: {batch.on_hold}")

    # Get details of a specific batch
    batch_details = await client.mgmt.rs.service.by_service_id(service_id).batch.by_client_batch_reference(batch_reference).get()
    print(f"Batch details: {batch_details.message_batch}")

    # Stop a batch
    stop_response = await client.mgmt.rs.service.by_service_id(service_id).batch.by_client_batch_reference(batch_reference).delete()
    print(f"Stopped {len(stop_response.stopped_messages)} messages")

asyncio.run(manage_batches())
```

## API Reference

### Main Client

- `MtHttpClient`: The main entry point for the SDK

### API Endpoints

The client provides access to different API versions and endpoints:

- `client.gw.rs.send_messages`: Send messages (recommended endpoint)
- `client.chimera.send_messages`: Alternative send messages endpoint
- `client.mgmt.rs.service`: Batch management operations
- `client.management`: Alternative batch management endpoint

### Models

All models are located in the `src/models/` directory:

- `GatewayRequest`: The main request object for sending messages
- `GatewayResponse`: Response containing batch reference and message statuses
- `Message`: Individual SMS message
- `Settings`: Message-level settings
- `MessageStatus`: Status information for sent messages
- `SendWindow`: Schedule messages for specific time windows
- `OriginatorSettings`: Configure message sender information
- `GasSettings`: GAS (Gateway API Service) configuration
- `Parameter`: Custom key-value parameters
- `BatchListResponse`: List of message batches
- `BatchSingleResponse`: Single batch details
- `StopBatchResponse`: Response when stopping a batch

### Request Builders

Request builders provide a fluent API for constructing requests:

- `SendMessagesRequestBuilder`: Build and execute send message requests
- `BatchRequestBuilder`: Build batch management requests
- Various service-specific builders in the `src/` directory structure

## Error Handling

The client uses Kiota's error handling mechanisms. HTTP errors are mapped to specific exception types:

```python
import asyncio
from src.models.problem_details import ProblemDetails

async def send_with_error_handling():
    try:
        response = await client.gw.rs.send_messages.post(request)
        print(f"Success! Batch: {response.batch_reference}")
    except Exception as e:
        if hasattr(e, 'error') and isinstance(e.error, ProblemDetails):
            print(f"API Error: {e.error.title}")
            print(f"Status: {e.error.status}")
            print(f"Detail: {e.error.detail}")
        else:
            print(f"Unexpected error: {e}")

asyncio.run(send_with_error_handling())
```

Common error status codes:

- `401 Unauthorized`: Invalid credentials
- `404 Not Found`: Batch or resource not found
- `400 Bad Request`: Invalid request parameters

## Testing

Install dev dependencies and run the full test suite:

```bash
uv sync
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

The tests live in `tests/unit/` and cover client initialization, all data models (field access, serialization, deserialization keys), and the request builders. See [docs/07-testing.md](docs/07-testing.md) for the full testing guide, including how to run specific tests, use fixtures, and write new tests.

## Migration from v2.x

If you're migrating from the previous `puzzel_sms_gateway_client` v2.x, here are the key differences:

### 1. Async/Await Required

The Kiota client is fully asynchronous:

**Old (v2.x):**

```python
response = client.send(messages=[message])
```

**New (Kiota):**

```python
response = await client.gw.rs.send_messages.post(request)
```

### 2. Client Initialization

**Old (v2.x):**

```python
import puzzel_sms_gateway_client as smsgw

client = smsgw.Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)
```

**New (Kiota):**

```python
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient

auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = BASE_ADDRESS

client = MtHttpClient(request_adapter)
```

### 3. Credentials in Request

Credentials are now part of each request rather than the client:

**Old (v2.x):**

```python
client = smsgw.Client(service_id=..., username=..., password=...)
client.send(messages=[...])
```

**New (Kiota):**

```python
request = GatewayRequest(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    message=[...]
)
await client.gw.rs.send_messages.post(request)
```

### 4. Model Structure

Models are now dataclasses with explicit typing:

**Old (v2.x):**

```python
message = smsgw.Message(
    recipient="+47...",
    content="Hello",
    settings=smsgw.MessageSettings(...)
)
```

**New (Kiota):**

```python
from src.models.message import Message
from src.models.settings import Settings

message = Message(
    recipient="+47...",
    content="Hello",
    settings=Settings(...)
)
```

### 5. Fluent API

The new client uses a fluent, path-based API:

```python
# Send messages
await client.gw.rs.send_messages.post(request)

# Manage batches
await client.mgmt.rs.service.by_service_id(123).batch.get()
await client.mgmt.rs.service.by_service_id(123).batch.by_client_batch_reference("ref").get()
await client.mgmt.rs.service.by_service_id(123).batch.by_client_batch_reference("ref").delete()
```

## Publishing

To build and publish the package to PyPI using `uv`:

```bash
# 1. Bump the version in pyproject.toml, then build
uv build

# 2. Publish to TestPyPI first (optional but recommended)
uv publish \
  --publish-url https://test.pypi.org/legacy/ \
  --token pypi-your-test-token-here

# 3. Publish to PyPI
uv publish --token pypi-your-production-token-here
```

For full details — credential storage, TestPyPI validation, version conventions, and `~/.pypirc` setup — see [docs/08-publishing.md](docs/08-publishing.md).

## Additional Documentation

For more detailed information, see the documentation in the `docs/` folder:

- [Documentation Index](docs/00-README.md) - Complete documentation index and navigation
- [uv Setup Guide](docs/01-uv-setup.md) - Complete guide for setting up with uv (recommended)
- [Getting Started Guide](docs/02-getting-started.md) - Step-by-step guide for beginners
- [Quick Reference](docs/03-quick-reference.md) - Cheat sheet for common operations
- [Complete Usage Examples](docs/04-examples.md) - More code examples and use cases
- [API Models Reference](docs/05-models.md) - Detailed model documentation
- [Advanced Topics](docs/06-advanced.md) - Configuration, customization, and best practices
- [Testing Guide](docs/07-testing.md) - Running tests, fixtures, and writing new tests
- [Publishing Guide](docs/08-publishing.md) - Building and publishing to PyPI with uv
- [Example Code Files](docs/examples/) - Runnable example scripts

## Support

For issues, questions, or contributions, please contact Puzzel support or refer to the main SMS Gateway documentation.

## License

Released under the MIT license. See [LICENSE](LICENSE) for details.
