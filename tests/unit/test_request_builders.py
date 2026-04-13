"""Tests for Kiota-generated request builders."""

from unittest.mock import MagicMock

import pytest
from kiota_abstractions.method import Method

from src.gw.rs.send_messages.send_messages_request_builder import (
    SendMessagesRequestBuilder,
)
from src.models.gateway_request import GatewayRequest
from src.models.message import Message
from src.mt_http_client import MtHttpClient


# ---------------------------------------------------------------------------
# SendMessagesRequestBuilder (gw)
# ---------------------------------------------------------------------------


@pytest.fixture
def send_messages_builder(mock_adapter: MagicMock) -> SendMessagesRequestBuilder:
    """Return a SendMessagesRequestBuilder with a mock adapter."""
    return SendMessagesRequestBuilder(
        mock_adapter,
        {"baseurl": "https://smsgw.puzzel.com"},
    )


@pytest.fixture
def minimal_gateway_request() -> GatewayRequest:
    """Return a minimal GatewayRequest for builder tests."""
    return GatewayRequest(
        service_id=12345,
        username="user",
        password="pass",
        message=[Message(recipient="+4799999999", content="Test")],
    )


@pytest.mark.asyncio
async def test_send_messages_post_raises_type_error_on_none_body(
    send_messages_builder: SendMessagesRequestBuilder,
) -> None:
    """post() should raise TypeError when body is None."""
    with pytest.raises(TypeError, match="body cannot be null"):
        await send_messages_builder.post(None)  # type: ignore[arg-type]


def test_send_messages_to_post_request_information_raises_on_none_body(
    send_messages_builder: SendMessagesRequestBuilder,
) -> None:
    """to_post_request_information raises TypeError when body is None."""
    with pytest.raises(TypeError, match="body cannot be null"):
        send_messages_builder.to_post_request_information(None)  # type: ignore[arg-type]


def test_send_messages_to_post_request_information_method(
    send_messages_builder: SendMessagesRequestBuilder,
    minimal_gateway_request: GatewayRequest,
) -> None:
    """to_post_request_information should produce a POST request."""
    request_info = send_messages_builder.to_post_request_information(
        minimal_gateway_request
    )
    assert request_info.http_method == Method.POST


def test_send_messages_to_post_request_information_accept_header(
    send_messages_builder: SendMessagesRequestBuilder,
    minimal_gateway_request: GatewayRequest,
) -> None:
    """to_post_request_information should include Accept: application/json."""
    request_info = send_messages_builder.to_post_request_information(
        minimal_gateway_request
    )
    assert request_info.headers.contains("Accept")
    assert "application/json" in request_info.headers.get("Accept")


def test_send_messages_to_get_request_information_method(
    send_messages_builder: SendMessagesRequestBuilder,
) -> None:
    """to_get_request_information should produce a GET request."""
    request_info = send_messages_builder.to_get_request_information()
    assert request_info.http_method == Method.GET


def test_send_messages_with_url_raises_on_none(
    send_messages_builder: SendMessagesRequestBuilder,
) -> None:
    """with_url raises TypeError when raw_url is None."""
    with pytest.raises(TypeError, match="raw_url cannot be null"):
        send_messages_builder.with_url(None)  # type: ignore[arg-type]


def test_send_messages_with_url_returns_new_builder(
    send_messages_builder: SendMessagesRequestBuilder,
    mock_adapter: MagicMock,
) -> None:
    """with_url should return a new SendMessagesRequestBuilder."""
    new_url = "https://other.smsgw.example.com/gw/rs/sendMessages"
    new_builder = send_messages_builder.with_url(new_url)
    assert isinstance(new_builder, SendMessagesRequestBuilder)
    assert new_builder is not send_messages_builder


# ---------------------------------------------------------------------------
# Client-level builder access (integration smoke tests)
# ---------------------------------------------------------------------------


def test_client_gw_send_messages_builder_type(
    client: MtHttpClient,
) -> None:
    """client.gw.rs.send_messages should return a SendMessagesRequestBuilder."""
    assert isinstance(
        client.gw.rs.send_messages, SendMessagesRequestBuilder
    )
