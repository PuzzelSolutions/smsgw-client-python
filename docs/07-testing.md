# Testing Guide

This guide covers how to run the test suite, understand the test structure, and write new tests for the Puzzel SMS Gateway Python Client.

## Contents

- [Requirements](#requirements)
- [Running Tests](#running-tests)
  - [All Tests](#all-tests)
  - [With Coverage](#with-coverage)
  - [Specific File or Test](#specific-file-or-test)
  - [By Keyword](#by-keyword)
- [Test Structure](#test-structure)
- [What Is Tested](#what-is-tested)
  - [Client Initialization](#client-initialization)
  - [Models](#models)
  - [Request Builders](#request-builders)
- [Fixtures](#fixtures)
- [Writing New Tests](#writing-new-tests)
  - [Sync Tests](#sync-tests)
  - [Async Tests](#async-tests)
  - [Parametrized Tests](#parametrized-tests)

---

## Requirements

Dev dependencies are declared in `pyproject.toml` under `[dependency-groups] dev` and installed automatically by `uv`:

| Package | Purpose |
| --- | --- |
| `pytest` | Test runner |
| `pytest-asyncio` | Async test support (`asyncio_mode = "auto"`) |
| `pytest-cov` | Coverage reporting |

Install them with:

```bash
uv sync
```

---

## Running Tests

All commands below should be run from the project root (`Generated/python/`).

### All Tests

```bash
uv run pytest
```

### With Coverage

```bash
uv run pytest --cov=src --cov-report=term-missing
```

To generate an HTML report in `htmlcov/`:

```bash
uv run pytest --cov=src --cov-report=html
```

### Specific File or Test

```bash
# Run a single test file
uv run pytest tests/unit/test_models.py

# Run a single test by name
uv run pytest tests/unit/test_models.py::test_message_default_values

# Run a single test by full path
uv run pytest tests/unit/test_client.py::test_client_raises_type_error_when_adapter_is_none
```

### By Keyword

```bash
# Run all tests whose name contains "originator"
uv run pytest -k originator

# Run all tests whose name contains "serialize"
uv run pytest -k serialize
```

---

## Test Structure

```text
tests/
└── unit/
    ├── conftest.py               # Shared fixtures
    ├── test_client.py            # MtHttpClient initialization and properties
    ├── test_models.py            # Data model field access and serialization
    └── test_request_builders.py  # Request building and HTTP method verification
```

`asyncio_mode = "auto"` is set in `pyproject.toml`, so any `async def test_*` function is automatically treated as an asyncio test — no `@pytest.mark.asyncio` decorator is needed.

---

## What Is Tested

### Client Initialization

[`tests/unit/test_client.py`](../tests/unit/test_client.py)

- `MtHttpClient(None)` raises `TypeError`
- Each route property (`gw`, `management`) returns the correct request-builder type
- The injected `request_adapter` is stored and accessible

### Models

[`tests/unit/test_models.py`](../tests/unit/test_models.py)

For every model (`OriginatorType`, `Message`, `OriginatorSettings`, `GasSettings`, `SendWindow`, `Parameter`, `Settings`, `GatewayRequest`, `GatewayResponse`, `MessageStatus`):

| Test category | What it verifies |
| --- | --- |
| Default values | All optional fields are `None` when not supplied |
| Field assignment | Values passed to the constructor are stored correctly |
| `create_from_discriminator_value(None)` | Raises `TypeError` |
| `serialize(None)` | Raises `TypeError` |
| `serialize(writer)` | Calls the writer with the correct camelCase JSON key for each field |
| `get_field_deserializers()` | Returns a dict whose keys match the camelCase JSON property names |

`OriginatorType` (enum) is additionally tested to confirm each member serialises to the expected string value.

### Request Builders

[`tests/unit/test_request_builders.py`](../tests/unit/test_request_builders.py)

- `post(None)` raises `TypeError` (async guard)
- `to_post_request_information(None)` raises `TypeError`
- `to_post_request_information(body)` returns a `RequestInformation` with `Method.POST` and an `Accept: application/json` header
- `to_get_request_information()` returns a `RequestInformation` with `Method.GET`
- `with_url(None)` raises `TypeError`
- `with_url(url)` returns a new `SendMessagesRequestBuilder` instance
- Smoke test confirming `client.gw.rs.send_messages` returns the correct builder type

---

## Fixtures

All shared fixtures are defined in [`tests/unit/conftest.py`](../tests/unit/conftest.py).

| Fixture | Type | Description |
| --- | --- | --- |
| `mock_adapter` | `MagicMock` | A mock `RequestAdapter` with `base_url` set and `get_serialization_writer_factory()` returning a `JsonSerializationWriterFactory` |
| `client` | `MtHttpClient` | A client built with `mock_adapter` |
| `basic_message` | `Message` | `recipient="+4799999999"`, `content="Hello from tests!"` |
| `originator_settings` | `OriginatorSettings` | International type with `originator="+4799999999"` |
| `gas_settings` | `GasSettings` | `service_code="01010"`, `description="Test service"` |
| `send_window` | `SendWindow` | Start `2024-01-15 08:00:00`, stop `2024-01-16 20:00:00` |
| `parameter` | `Parameter` | `key="someKey"`, `value="someValue"` |
| `settings` | `Settings` | Fully populated using the fixtures above |
| `gateway_request` | `GatewayRequest` | Uses `basic_message`, `SERVICE_ID=12345`, `BATCH_REFERENCE="test-batch-001"` |
| `message_status` | `MessageStatus` | `status_code=200`, `message_id="msg-001"` |
| `gateway_response` | `GatewayResponse` | `batch_reference="test-batch-001"` with one `message_status` |

---

## Writing New Tests

### Sync Tests

```python
from src.models.message import Message

def test_message_has_correct_recipient() -> None:
    msg = Message(recipient="+4799999999")
    assert msg.recipient == "+4799999999"
```

### Async Tests

Because `asyncio_mode = "auto"`, simply declare the function as `async`:

```python
import pytest
from src.gw.rs.send_messages.send_messages_request_builder import (
    SendMessagesRequestBuilder,
)

async def test_post_raises_on_none_body(
    send_messages_builder: SendMessagesRequestBuilder,
) -> None:
    with pytest.raises(TypeError):
        await send_messages_builder.post(None)
```

### Parametrized Tests

Use `@pytest.mark.parametrize` to cover multiple inputs with a single test function:

```python
import pytest
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType

@pytest.mark.parametrize(
    "originator,originator_type",
    [
        ("+4799999999", OriginatorType.International),
        ("Puzzel",      OriginatorType.Alphanumeric),
        ("1960",        OriginatorType.Network),
    ],
)
def test_originator_settings(
    originator: str,
    originator_type: OriginatorType,
) -> None:
    settings = OriginatorSettings(
        originator=originator,
        originator_type=originator_type,
    )
    assert settings.originator == originator
    assert settings.originator_type == originator_type
```
