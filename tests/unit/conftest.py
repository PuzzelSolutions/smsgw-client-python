"""Fixtures and test data automatically loaded by pytest."""

from unittest.mock import MagicMock

import pytest
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_serialization_json.json_serialization_writer_factory import (
    JsonSerializationWriterFactory,
)

from src.models.gas_settings import GasSettings
from src.models.gateway_request import GatewayRequest
from src.models.gateway_response import GatewayResponse
from src.models.message import Message
from src.models.message_status import MessageStatus
from src.models.originator_settings import OriginatorSettings
from src.models.originator_type import OriginatorType
from src.models.parameter import Parameter
from src.models.send_window import SendWindow
from src.models.settings import Settings
from src.mt_http_client import MtHttpClient

BASE_URL = "https://smsgw.puzzel.com"
SERVICE_ID = 12345
USERNAME = "test_user"
PASSWORD = "test_password"
RECIPIENT = "+4799999999"
BATCH_REFERENCE = "test-batch-001"


@pytest.fixture
def mock_adapter() -> MagicMock:
    """Return a mock RequestAdapter."""
    adapter = MagicMock(spec=RequestAdapter)
    adapter.base_url = BASE_URL
    adapter.get_serialization_writer_factory.return_value = (
        JsonSerializationWriterFactory()
    )
    return adapter


@pytest.fixture
def client(mock_adapter: MagicMock) -> MtHttpClient:
    """Return a MtHttpClient with a mock adapter."""
    return MtHttpClient(mock_adapter)


@pytest.fixture
def basic_message() -> Message:
    """Return a basic Message."""
    return Message(recipient=RECIPIENT, content="Hello from tests!")


@pytest.fixture
def originator_settings() -> OriginatorSettings:
    """Return OriginatorSettings with international type."""
    return OriginatorSettings(
        originator=RECIPIENT,
        originator_type=OriginatorType.International,
    )


@pytest.fixture
def gas_settings() -> GasSettings:
    """Return a GasSettings instance."""
    return GasSettings(service_code="01010", description="Test service")


@pytest.fixture
def send_window() -> SendWindow:
    """Return a SendWindow instance."""
    return SendWindow(
        start_date="2024-01-15",
        start_time="08:00:00",
        stop_date="2024-01-16",
        stop_time="20:00:00",
    )


@pytest.fixture
def parameter() -> Parameter:
    """Return a Parameter instance."""
    return Parameter(key="someKey", value="someValue")


@pytest.fixture
def settings(
    originator_settings: OriginatorSettings,
    gas_settings: GasSettings,
    send_window: SendWindow,
    parameter: Parameter,
) -> Settings:
    """Return a fully populated Settings instance."""
    return Settings(
        originator_settings=originator_settings,
        gas_settings=gas_settings,
        send_window=send_window,
        parameter=[parameter],
        priority=1,
        validity=120,
        auto_detect_encoding=True,
    )


@pytest.fixture
def gateway_request(basic_message: Message) -> GatewayRequest:
    """Return a GatewayRequest."""
    return GatewayRequest(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        batch_reference=BATCH_REFERENCE,
        message=[basic_message],
    )


@pytest.fixture
def message_status() -> MessageStatus:
    """Return a MessageStatus."""
    return MessageStatus(
        message_id="msg-001",
        recipient=RECIPIENT,
        status_code=200,
        status_message="OK",
        sequence_index=1,
        client_reference="ref-001",
        session_id="session-001",
    )


@pytest.fixture
def gateway_response(message_status: MessageStatus) -> GatewayResponse:
    """Return a GatewayResponse."""
    return GatewayResponse(
        batch_reference=BATCH_REFERENCE,
        message_status=[message_status],
    )
