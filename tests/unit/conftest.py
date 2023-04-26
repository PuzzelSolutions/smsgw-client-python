"""Test data, functions, and fixtures automatically loaded by pytest."""

import pytest
from puzzel_sms_gateway_client import (
    Client,
    Message,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
)


SERVICE_ID = 1000
USERNAME = "admin"
PASSWORD = "puzzel"
BASE_ADDRESS = "https://[YOUR_SERVER_ADDRESS]/gw/rs"
SEND_MESSAGES_ENDPOINT: str = "/sendMessages"
HEADERS: dict[str, str] = {
    "Accept": "application/json",
    "Content-type": "application/json",
}


@pytest.fixture
def client_values():
    """Return client values for the test."""
    return {
        "SERVICE_ID": SERVICE_ID,
        "USERNAME": USERNAME,
        "PASSWORD": PASSWORD,
        "BASE_ADDRESS": BASE_ADDRESS,
        "SEND_MESSAGES_ENDPOINT": SEND_MESSAGES_ENDPOINT,
        "HEADERS": HEADERS,
    }


@pytest.fixture
def client():
    """Return a client."""
    return Client(
        service_id=SERVICE_ID,
        username=USERNAME,
        password=PASSWORD,
        base_address=BASE_ADDRESS,
    )
