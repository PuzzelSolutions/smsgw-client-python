"""Tests for MtHttpClient initialization and properties."""

from unittest.mock import MagicMock

import pytest

from src.gw.gw_request_builder import GwRequestBuilder
from src.management.management_request_builder import ManagementRequestBuilder
from src.mt_http_client import MtHttpClient


def test_client_raises_type_error_when_adapter_is_none() -> None:
    """MtHttpClient must raise TypeError if request_adapter is None."""
    with pytest.raises(TypeError, match="request_adapter cannot be null"):
        MtHttpClient(None)  # type: ignore[arg-type]


def test_client_initializes_with_valid_adapter(
    mock_adapter: MagicMock,
) -> None:
    """MtHttpClient should initialize without errors given a valid adapter."""
    client = MtHttpClient(mock_adapter)
    assert client is not None


def test_client_gw_property_returns_builder(
    client: MtHttpClient,
) -> None:
    """The gw property should return a GwRequestBuilder."""
    assert isinstance(client.gw, GwRequestBuilder)


def test_client_management_property_returns_builder(
    client: MtHttpClient,
) -> None:
    """The management property should return a ManagementRequestBuilder."""
    assert isinstance(client.management, ManagementRequestBuilder)


def test_client_stores_request_adapter(mock_adapter: MagicMock) -> None:
    """MtHttpClient should expose the adapter via request_adapter."""
    client = MtHttpClient(mock_adapter)
    assert client.request_adapter is mock_adapter
