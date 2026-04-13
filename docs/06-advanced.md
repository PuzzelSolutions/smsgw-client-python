# Advanced Topics

This document covers advanced usage patterns, configuration options, and best practices for the Puzzel SMS Gateway Python Client.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Request Adapters](#request-adapters)
- [Authentication](#authentication)
- [Custom Headers and Configuration](#custom-headers-and-configuration)
- [Middleware](#middleware)
- [Timeout and Retry Configuration](#timeout-and-retry-configuration)
- [Connection Pooling](#connection-pooling)
- [Testing](#testing)
- [Performance Optimization](#performance-optimization)
- [Security Best Practices](#security-best-practices)
- [Monitoring and Observability](#monitoring-and-observability)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The Puzzel SMS Gateway Python Client is built on Microsoft Kiota, which provides a layered architecture:

```text
┌─────────────────────────────────────┐
│      Your Application Code          │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│       MtHttpClient (API Client)     │
│  - Fluent API (gw, management)       │
│  - Request Builders                 │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Request Adapter Layer          │
│  - HTTP Communication               │
│  - Serialization/Deserialization    │
│  - Authentication                   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│     HTTP Client (httpx/aiohttp)     │
│  - Network Communication            │
│  - Connection Management            │
└─────────────────────────────────────┘
```

### Key Components

1. **MtHttpClient**: Main entry point, provides fluent API
2. **Request Builders**: Build and execute API requests
3. **Request Adapter**: Handles HTTP communication and serialization
4. **Models**: Data classes representing API objects
5. **Authentication Provider**: Manages authentication

## Request Adapters

The request adapter is the bridge between the API client and the HTTP layer.

### Default Adapter (httpx)

```python
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from kiota_abstractions.authentication import AnonymousAuthenticationProvider

auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(auth_provider)
request_adapter.base_url = "https://your-gateway-server.com"
```

### Custom Adapter Configuration

```python
import httpx
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

# Create custom httpx client with specific configuration
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0, connect=10.0),
    limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
    verify=True,  # SSL verification
    http2=True    # Enable HTTP/2
)

# Use custom client with adapter
auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(
    auth_provider,
    http_client=http_client
)
request_adapter.base_url = "https://your-gateway-server.com"
```

### Alternative: aiohttp Adapter

If you prefer aiohttp over httpx:

```python
# Note: This requires kiota-http-aiohttp package
from kiota_http_aiohttp import AioHttpRequestAdapter
from kiota_abstractions.authentication import AnonymousAuthenticationProvider

auth_provider = AnonymousAuthenticationProvider()
request_adapter = AioHttpRequestAdapter(auth_provider)
request_adapter.base_url = "https://your-gateway-server.com"
```

## Authentication

### Current Authentication (Body-based)

The SMS Gateway uses credentials in the request body:

```python
from kiota_abstractions.authentication import AnonymousAuthenticationProvider

# Use AnonymousAuthenticationProvider since auth is in request body
auth_provider = AnonymousAuthenticationProvider()
request_adapter = HttpxRequestAdapter(auth_provider)
```

### Custom Authentication Provider

If you need to implement custom authentication logic:

```python
from kiota_abstractions.authentication import AuthenticationProvider
from kiota_abstractions.request_information import RequestInformation
from typing import Dict, Set

class CustomAuthProvider(AuthenticationProvider):
    """Custom authentication provider."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def authenticate_request(
        self,
        request: RequestInformation,
        additional_authentication_context: Dict[str, object] = None
    ) -> None:
        """Add custom authentication to request."""
        # Example: Add API key header
        request.headers.add("X-API-Key", self.api_key)

# Usage
auth_provider = CustomAuthProvider("your-api-key")
request_adapter = HttpxRequestAdapter(auth_provider)
```

### Credential Management

Store credentials securely:

```python
import os
from dataclasses import dataclass

@dataclass
class Credentials:
    """Secure credential storage."""
    service_id: int
    username: str
    password: str
    
    @classmethod
    def from_env(cls) -> "Credentials":
        """Load credentials from environment variables."""
        return cls(
            service_id=int(os.getenv("SMS_SERVICE_ID")),
            username=os.getenv("SMS_USERNAME"),
            password=os.getenv("SMS_PASSWORD")
        )
    
    @classmethod
    def from_file(cls, path: str) -> "Credentials":
        """Load credentials from secure file."""
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(**data)

# Usage
creds = Credentials.from_env()
```

## Custom Headers and Configuration

### Adding Custom Headers

```python
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.base_request_configuration import RequestConfiguration

# Create request configuration with custom headers
config = RequestConfiguration()
config.headers.add("X-Custom-Header", "custom-value")
config.headers.add("X-Request-ID", "unique-request-id")

# Use in request
response = await client.gw.rs.send_messages.post(request, request_configuration=config)
```

### Request Options

```python
from kiota_abstractions.request_option import RequestOption

class CustomRequestOption(RequestOption):
    """Custom request option."""
    
    def __init__(self, custom_value: str):
        self.custom_value = custom_value

# Add to request configuration
config = RequestConfiguration()
config.options.append(CustomRequestOption("value"))
```

## Middleware

Middleware allows you to intercept and modify requests/responses.

### Custom Middleware

```python
from kiota_abstractions.middleware import BaseMiddleware
from kiota_abstractions.request_information import RequestInformation
from typing import Callable, Awaitable

class LoggingMiddleware(BaseMiddleware):
    """Middleware that logs all requests and responses."""
    
    async def send(
        self,
        request: RequestInformation,
        next_middleware: Callable[[RequestInformation], Awaitable[any]]
    ) -> any:
        """Intercept and log request/response."""
        import logging
        logger = logging.getLogger(__name__)
        
        # Log request
        logger.info(f"Request: {request.http_method} {request.url}")
        
        try:
            # Call next middleware
            response = await next_middleware(request)
            
            # Log response
            logger.info(f"Response: Success")
            
            return response
        except Exception as e:
            # Log error
            logger.error(f"Response: Error - {e}")
            raise

# Add middleware to adapter
from kiota_http.middleware import MiddlewarePipeline

middleware = [LoggingMiddleware()]
pipeline = MiddlewarePipeline(middleware)
# Configure adapter with pipeline
```

### Rate Limiting Middleware

```python
import asyncio
from datetime import datetime, timedelta

class RateLimitMiddleware(BaseMiddleware):
    """Middleware that enforces rate limiting."""
    
    def __init__(self, max_requests: int, time_window: timedelta):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def send(
        self,
        request: RequestInformation,
        next_middleware: Callable[[RequestInformation], Awaitable[any]]
    ) -> any:
        """Enforce rate limit."""
        now = datetime.now()
        
        # Remove old requests outside time window
        self.requests = [
            req_time for req_time in self.requests
            if now - req_time < self.time_window
        ]
        
        # Check rate limit
        if len(self.requests) >= self.max_requests:
            # Calculate wait time
            oldest = min(self.requests)
            wait_until = oldest + self.time_window
            wait_seconds = (wait_until - now).total_seconds()
            
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
        
        # Record request
        self.requests.append(now)
        
        # Continue with request
        return await next_middleware(request)

# Usage: 100 requests per minute
rate_limiter = RateLimitMiddleware(
    max_requests=100,
    time_window=timedelta(minutes=1)
)
```

## Timeout and Retry Configuration

### Timeout Configuration

```python
import httpx
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

# Configure timeouts
timeout_config = httpx.Timeout(
    timeout=30.0,      # Total timeout
    connect=10.0,      # Connection timeout
    read=20.0,         # Read timeout
    write=10.0,        # Write timeout
    pool=5.0           # Pool timeout
)

http_client = httpx.AsyncClient(timeout=timeout_config)
request_adapter = HttpxRequestAdapter(auth_provider, http_client=http_client)
```

### Retry Configuration

```python
from httpx import AsyncClient, Limits
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

class RetryableClient:
    """Client with automatic retry logic."""
    
    def __init__(self, client: MtHttpClient, max_retries: int = 3):
        self.client = client
        self.max_retries = max_retries
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError))
    )
    async def send_with_retry(self, request):
        """Send request with automatic retry."""
        return await self.client.gw.rs.send_messages.post(request)

# Usage
retryable_client = RetryableClient(client)
response = await retryable_client.send_with_retry(request)
```

## Connection Pooling

### Configure Connection Pool

```python
import httpx

# Configure connection limits
limits = httpx.Limits(
    max_keepalive_connections=20,  # Keep-alive connections
    max_connections=100,            # Total connections
    keepalive_expiry=30.0          # Keep-alive timeout
)

http_client = httpx.AsyncClient(limits=limits)
request_adapter = HttpxRequestAdapter(auth_provider, http_client=http_client)
```

### Connection Pool Monitoring

```python
class ConnectionPoolMonitor:
    """Monitor connection pool usage."""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
    
    def get_stats(self) -> dict:
        """Get connection pool statistics."""
        # Note: Actual implementation depends on httpx internals
        return {
            "active_connections": len(self.http_client._transport._pool._connections),
            "idle_connections": len(self.http_client._transport._pool._idle_connections),
        }

# Usage
monitor = ConnectionPoolMonitor(http_client)
print(monitor.get_stats())
```

## Testing

### Mock Client for Testing

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.models.gateway_response import GatewayResponse
from src.models.message_status import MessageStatus

@pytest.fixture
def mock_client():
    """Create mock SMS client for testing."""
    client = MagicMock()
    
    # Mock successful response
    mock_response = GatewayResponse()
    mock_response.batch_reference = "test-batch-123"
    mock_response.message_status = [
        MessageStatus(
            status_code=1,
            status_message="Message enqueued",
            recipient="+47xxxxxxxxx",
            message_id="msg-123",
            sequence_index=1
        )
    ]
    
    # Configure mock
    client.gw.rs.send_messages.post = AsyncMock(return_value=mock_response)
    
    return client

@pytest.mark.asyncio
async def test_send_sms(mock_client):
    """Test sending SMS."""
    from src.models.gateway_request import GatewayRequest
    from src.models.message import Message
    
    request = GatewayRequest(
        service_id=12345,
        username="test",
        password="test",
        message=[Message(recipient="+47xxxxxxxxx", content="Test")]
    )
    
    response = await mock_client.gw.rs.send_messages.post(request)
    
    assert response.batch_reference == "test-batch-123"
    assert len(response.message_status) == 1
    assert response.message_status[0].status_code == 1
```

### Integration Testing

```python
import pytest
import os

@pytest.fixture
def integration_client():
    """Create real client for integration tests."""
    if not os.getenv("RUN_INTEGRATION_TESTS"):
        pytest.skip("Integration tests disabled")
    
    from kiota_abstractions.authentication import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter
    from src.mt_http_client import MtHttpClient
    
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = os.getenv("SMS_GATEWAY_URL")
    
    return MtHttpClient(request_adapter)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_send_real_sms(integration_client):
    """Integration test with real SMS Gateway."""
    from src.models.gateway_request import GatewayRequest
    from src.models.message import Message
    
    request = GatewayRequest(
        service_id=int(os.getenv("SMS_SERVICE_ID")),
        username=os.getenv("SMS_USERNAME"),
        password=os.getenv("SMS_PASSWORD"),
        message=[
            Message(
                recipient=os.getenv("TEST_PHONE_NUMBER"),
                content="Integration test message"
            )
        ]
    )
    
    response = await integration_client.gw.rs.send_messages.post(request)
    
    assert response.batch_reference is not None
    assert len(response.message_status) == 1
    assert response.message_status[0].status_code == 1
```

### Test Fixtures

```python
import pytest
from typing import AsyncGenerator

@pytest.fixture
async def sms_client() -> AsyncGenerator[MtHttpClient, None]:
    """Async fixture for SMS client with cleanup."""
    from kiota_abstractions.authentication import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter
    from src.mt_http_client import MtHttpClient
    
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = "https://test-server.com"
    
    client = MtHttpClient(request_adapter)
    
    yield client
    
    # Cleanup
    # Close connections, etc.
```

## Performance Optimization

### Batch Message Sending

```python
async def send_messages_in_batches(
    client: MtHttpClient,
    config: Credentials,
    recipients: list[str],
    content: str,
    batch_size: int = 1000
):
    """Send messages in optimal batches."""
    from src.models.gateway_request import GatewayRequest
    from src.models.message import Message
    
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        
        messages = [
            Message(recipient=r, content=content)
            for r in batch
        ]
        
        request = GatewayRequest(
            service_id=config.service_id,
            username=config.username,
            password=config.password,
            batch_reference=f"batch-{i // batch_size}",
            message=messages
        )
        
        response = await client.gw.rs.send_messages.post(request)
        print(f"Batch {i // batch_size}: {len(response.message_status)} sent")
```

### Concurrent Requests

```python
import asyncio
from typing import List

async def send_concurrent_batches(
    client: MtHttpClient,
    config: Credentials,
    batches: List[List[str]],
    content: str,
    max_concurrent: int = 5
):
    """Send multiple batches concurrently with limit."""
    from src.models.gateway_request import GatewayRequest
    from src.models.message import Message
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def send_batch(batch_id: int, recipients: List[str]):
        async with semaphore:
            messages = [Message(recipient=r, content=content) for r in recipients]
            request = GatewayRequest(
                service_id=config.service_id,
                username=config.username,
                password=config.password,
                batch_reference=f"concurrent-{batch_id}",
                message=messages
            )
            return await client.gw.rs.send_messages.post(request)
    
    tasks = [send_batch(i, batch) for i, batch in enumerate(batches)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    return responses
```

### Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedBatchInfo:
    """Cache batch information to reduce API calls."""
    
    def __init__(self, client: MtHttpClient, cache_ttl: timedelta = timedelta(minutes=5)):
        self.client = client
        self.cache_ttl = cache_ttl
        self._cache = {}
    
    async def get_batch_info(self, service_id: int, batch_ref: str):
        """Get batch info with caching."""
        cache_key = f"{service_id}:{batch_ref}"
        
        # Check cache
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if datetime.now() - cached_time < self.cache_ttl:
                return cached_data
        
        # Fetch from API
        batch_info = await self.client.management.by_service_id(service_id).batch.by_client_batch_reference(batch_ref).get()
        
        # Update cache
        self._cache[cache_key] = (datetime.now(), batch_info)
        
        return batch_info
```

## Security Best Practices

### Secure Credential Storage

```python
import keyring
from cryptography.fernet import Fernet

class SecureCredentialStore:
    """Secure credential storage using system keyring."""
    
    SERVICE_NAME = "puzzel-sms-gateway"
    
    @staticmethod
    def store_credentials(username: str, password: str, service_id: int):
        """Store credentials securely."""
        keyring.set_password(SecureCredentialStore.SERVICE_NAME, "username", username)
        keyring.set_password(SecureCredentialStore.SERVICE_NAME, "password", password)
        keyring.set_password(SecureCredentialStore.SERVICE_NAME, "service_id", str(service_id))
    
    @staticmethod
    def get_credentials() -> tuple[str, str, int]:
        """Retrieve credentials securely."""
        username = keyring.get_password(SecureCredentialStore.SERVICE_NAME, "username")
        password = keyring.get_password(SecureCredentialStore.SERVICE_NAME, "password")
        service_id = int(keyring.get_password(SecureCredentialStore.SERVICE_NAME, "service_id"))
        return username, password, service_id
```

### Input Validation

```python
import re
from typing import Optional

class InputValidator:
    """Validate input before sending to API."""
    
    PHONE_PATTERN = re.compile(r'^\+\d{10,15}$')
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate phone number format."""
        return bool(InputValidator.PHONE_PATTERN.match(phone))
    
    @staticmethod
    def validate_message_content(content: str) -> tuple[bool, Optional[str]]:
        """Validate message content."""
        if not content:
            return False, "Content cannot be empty"
        
        if len(content) > 1600:
            return False, f"Content too long: {len(content)} chars (max 1600)"
        
        return True, None
    
    @staticmethod
    def sanitize_content(content: str) -> str:
        """Sanitize message content."""
        # Remove control characters
        sanitized = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
        return sanitized
```

### SSL/TLS Configuration

```python
import ssl
import httpx

# Create secure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Configure httpx with SSL context
http_client = httpx.AsyncClient(verify=ssl_context)
request_adapter = HttpxRequestAdapter(auth_provider, http_client=http_client)
```

## Monitoring and Observability

### Structured Logging

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging for SMS operations."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_sms_sent(self, batch_ref: str, recipient_count: int, success: bool):
        """Log SMS send operation."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "event": "sms_sent",
            "batch_reference": batch_ref,
            "recipient_count": recipient_count,
            "success": success
        }
        self.logger.info(json.dumps(log_data))
    
    def log_error(self, error_type: str, error_message: str, context: dict):
        """Log error with context."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "event": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        self.logger.error(json.dumps(log_data))
```

### Metrics Collection

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

@dataclass
class SmsMetrics:
    """Collect and track SMS metrics."""
    
    total_sent: int = 0
    total_failed: int = 0
    total_batches: int = 0
    response_times: List[float] = field(default_factory=list)
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    
    def record_send(self, success: bool, response_time: float):
        """Record send operation."""
        if success:
            self.total_sent += 1
        else:
            self.total_failed += 1
        
        self.response_times.append(response_time)
    
    def record_error(self, error_type: str):
        """Record error."""
        self.errors_by_type[error_type] = self.errors_by_type.get(error_type, 0) + 1
    
    def get_average_response_time(self) -> float:
        """Calculate average response time."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_success_rate(self) -> float:
        """Calculate success rate."""
        total = self.total_sent + self.total_failed
        if total == 0:
            return 0.0
        return self.total_sent / total
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add span processor
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

async def send_with_tracing(client, request):
    """Send SMS with distributed tracing."""
    with tracer.start_as_current_span("send_sms") as span:
        span.set_attribute("service_id", request.service_id)
        span.set_attribute("message_count", len(request.message))
        
        try:
            response = await client.gw.rs.send_messages.post(request)
            span.set_attribute("batch_reference", response.batch_reference)
            span.set_attribute("success", True)
            return response
        except Exception as e:
            span.set_attribute("success", False)
            span.set_attribute("error", str(e))
            raise
```

## Troubleshooting

### Common Issues

#### 1. Connection Timeout

```python
# Increase timeout
timeout = httpx.Timeout(60.0, connect=20.0)
http_client = httpx.AsyncClient(timeout=timeout)
```

#### 2. SSL Certificate Errors

```python
# Disable SSL verification (not recommended for production)
http_client = httpx.AsyncClient(verify=False)

# Or provide custom CA bundle
http_client = httpx.AsyncClient(verify="/path/to/ca-bundle.crt")
```

#### 3. Authentication Failures

```python
# Verify credentials
print(f"Service ID: {config.service_id}")
print(f"Username: {config.username}")
print(f"Password: {'*' * len(config.password)}")

# Test with simple request
try:
    response = await client.gw.rs.send_messages.post(request)
except Exception as e:
    if hasattr(e, 'error') and e.error.status == 401:
        print("Authentication failed - check credentials")
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("kiota").setLevel(logging.DEBUG)

# Now all requests/responses will be logged
```

### Request/Response Inspection

```python
class DebugMiddleware(BaseMiddleware):
    """Middleware for debugging requests and responses."""
    
    async def send(self, request, next_middleware):
        print(f"\n=== REQUEST ===")
        print(f"Method: {request.http_method}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        
        try:
            response = await next_middleware(request)
            print(f"\n=== RESPONSE ===")
            print(f"Success")
            return response
        except Exception as e:
            print(f"\n=== ERROR ===")
            print(f"Error: {e}")
            raise
```

## Summary

This document covered:

- Architecture and components
- Request adapters and configuration
- Authentication patterns
- Middleware and interceptors
- Timeout and retry strategies
- Connection pooling
- Testing approaches
- Performance optimization
- Security best practices
- Monitoring and observability
- Troubleshooting techniques

For more information, see:

- [Main README](../README.md) - Main documentation
- [04 - Examples](04-examples.md) - Usage examples
- [05 - Models](05-models.md) - API models reference
