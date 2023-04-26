"""Test the client for the SMS Gateway."""

###############################################################################
###############################################################################
###############################################################################
# Test exceptions
###############################################################################
###############################################################################


def test_client_init(client, client_values):
    """Test the client initialization."""
    assert client.base_address == client_values["BASE_ADDRESS"]
    assert client.service_id == client_values["SERVICE_ID"]
    assert client.username == client_values["USERNAME"]
    assert client.password == client_values["PASSWORD"]
    assert client.batch_reference is None
    assert client.HEADERS == client_values["HEADERS"]
    assert (
        client.SEND_MESSAGES_ENDPOINT
        == client_values["SEND_MESSAGES_ENDPOINT"]
    )
    assert client.send_messages_url == (
        f"{client_values['BASE_ADDRESS']}"
        f"{client_values['SEND_MESSAGES_ENDPOINT']}"
    )
