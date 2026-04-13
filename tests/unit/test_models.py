"""Tests for Kiota-generated data models."""

from unittest.mock import MagicMock

import pytest

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

# ---------------------------------------------------------------------------
# OriginatorType enum
# ---------------------------------------------------------------------------


def test_originator_type_international_value() -> None:
    """OriginatorType.International should serialise to 'International'."""
    assert OriginatorType.International.value == "International"


def test_originator_type_alphanumeric_value() -> None:
    """OriginatorType.Alphanumeric should serialise to 'Alphanumeric'."""
    assert OriginatorType.Alphanumeric.value == "Alphanumeric"


def test_originator_type_network_value() -> None:
    """OriginatorType.Network should serialise to 'Network'."""
    assert OriginatorType.Network.value == "Network"


def test_originator_type_has_three_members() -> None:
    """OriginatorType should have exactly three members."""
    assert len(OriginatorType) == 3


# ---------------------------------------------------------------------------
# Message
# ---------------------------------------------------------------------------


def test_message_default_values() -> None:
    """Message fields should default to None."""
    msg = Message()
    assert msg.recipient is None
    assert msg.content is None
    assert msg.client_reference is None
    assert msg.price is None
    assert msg.price_xml is None
    assert msg.settings is None


@pytest.mark.parametrize(
    "recipient,content,client_reference",
    [
        ("+4799999999", "Hello!", "ref-001"),
        ("+4700000000", "Test message", None),
        ("+4711111111", "", "ref-002"),
    ],
)
def test_message_field_assignment(
    recipient: str,
    content: str,
    client_reference: str | None,
) -> None:
    """Message should store all assigned field values correctly."""
    msg = Message(
        recipient=recipient,
        content=content,
        client_reference=client_reference,
    )
    assert msg.recipient == recipient
    assert msg.content == content
    assert msg.client_reference == client_reference


def test_message_create_from_discriminator_value_raises_on_none() -> None:
    """create_from_discriminator_value raises TypeError when parse_node is None."""
    with pytest.raises(TypeError, match="parse_node cannot be null"):
        Message.create_from_discriminator_value(None)  # type: ignore[arg-type]


def test_message_create_from_discriminator_value_returns_instance() -> None:
    """create_from_discriminator_value should return a Message instance."""
    mock_node = MagicMock()
    result = Message.create_from_discriminator_value(mock_node)
    assert isinstance(result, Message)


def test_message_serialize_raises_on_none_writer() -> None:
    """Message.serialize raises TypeError when writer is None."""
    msg = Message(recipient="+4799999999", content="Hi")
    with pytest.raises(TypeError, match="writer cannot be null"):
        msg.serialize(None)  # type: ignore[arg-type]


def test_message_serialize_writes_all_fields() -> None:
    """Message.serialize should call writer for every field."""
    msg = Message(
        recipient="+4799999999",
        content="Hi",
        client_reference="ref-001",
        price=100,
        price_xml="<price/>",
    )
    writer = MagicMock()
    msg.serialize(writer)

    writer.write_str_value.assert_any_call("clientReference", "ref-001")
    writer.write_str_value.assert_any_call("content", "Hi")
    writer.write_int_value.assert_any_call("price", 100)
    writer.write_str_value.assert_any_call("priceXml", "<price/>")
    writer.write_str_value.assert_any_call("recipient", "+4799999999")


def test_message_get_field_deserializers_keys() -> None:
    """Message deserializer dict should contain the correct camelCase keys."""
    msg = Message()
    keys = set(msg.get_field_deserializers().keys())
    assert keys == {
        "clientReference",
        "content",
        "price",
        "priceXml",
        "recipient",
        "settings",
    }


# ---------------------------------------------------------------------------
# OriginatorSettings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "originator,originator_type",
    [
        ("+4799999999", OriginatorType.International),
        ("Puzzel", OriginatorType.Alphanumeric),
        ("1960", OriginatorType.Network),
    ],
)
def test_originator_settings_field_assignment(
    originator: str,
    originator_type: OriginatorType,
) -> None:
    """OriginatorSettings should store originator and originator_type."""
    settings = OriginatorSettings(
        originator=originator,
        originator_type=originator_type,
    )
    assert settings.originator == originator
    assert settings.originator_type == originator_type
    assert settings.originator is not None
    assert settings.originator_type is not None


def test_originator_settings_default_values() -> None:
    """OriginatorSettings fields should default to None."""
    settings = OriginatorSettings()
    assert settings.originator is None
    assert settings.originator_type is None


def test_originator_settings_create_from_discriminator_value_raises_on_none() -> None:
    """create_from_discriminator_value raises TypeError when parse_node is None."""
    with pytest.raises(TypeError):
        OriginatorSettings.create_from_discriminator_value(None)  # type: ignore[arg-type]


def test_originator_settings_serialize_raises_on_none_writer() -> None:
    """OriginatorSettings.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        OriginatorSettings().serialize(None)  # type: ignore[arg-type]


def test_originator_settings_serialize_writes_fields() -> None:
    """OriginatorSettings.serialize writes originator and originatorType."""
    settings = OriginatorSettings(
        originator="Puzzel",
        originator_type=OriginatorType.Alphanumeric,
    )
    writer = MagicMock()
    settings.serialize(writer)

    writer.write_str_value.assert_called_once_with("originator", "Puzzel")
    writer.write_enum_value.assert_called_once_with(
        "originatorType", OriginatorType.Alphanumeric
    )


def test_originator_settings_deserializer_keys() -> None:
    """OriginatorSettings deserializer keys should be camelCase."""
    keys = set(OriginatorSettings().get_field_deserializers().keys())
    assert keys == {"originator", "originatorType"}


# ---------------------------------------------------------------------------
# GasSettings
# ---------------------------------------------------------------------------


def test_gas_settings_field_assignment() -> None:
    """GasSettings should store service_code and description correctly."""
    gs = GasSettings(service_code="01010", description="Test")
    assert gs.service_code == "01010"
    assert gs.description == "Test"
    assert len(gs.service_code) == 5


def test_gas_settings_default_values() -> None:
    """GasSettings fields should default to None."""
    gs = GasSettings()
    assert gs.service_code is None
    assert gs.description is None


def test_gas_settings_serialize_writes_fields() -> None:
    """GasSettings.serialize writes serviceCode and description."""
    gs = GasSettings(service_code="01010", description="Desc")
    writer = MagicMock()
    gs.serialize(writer)

    writer.write_str_value.assert_any_call("serviceCode", "01010")
    writer.write_str_value.assert_any_call("description", "Desc")


def test_gas_settings_deserializer_keys() -> None:
    """GasSettings deserializer keys should be camelCase."""
    keys = set(GasSettings().get_field_deserializers().keys())
    assert keys == {"serviceCode", "description"}


def test_gas_settings_create_from_discriminator_value_raises_on_none() -> None:
    """create_from_discriminator_value raises TypeError when parse_node is None."""
    with pytest.raises(TypeError):
        GasSettings.create_from_discriminator_value(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# SendWindow
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "start_date,start_time,stop_date,stop_time",
    [
        ("2024-01-15", "08:00:00", "2024-01-16", "20:00:00"),
        ("2024-07-01", "00:00:00", None, None),
    ],
)
def test_send_window_field_assignment(
    start_date: str,
    start_time: str,
    stop_date: str | None,
    stop_time: str | None,
) -> None:
    """SendWindow should store all date/time fields correctly."""
    sw = SendWindow(
        start_date=start_date,
        start_time=start_time,
        stop_date=stop_date,
        stop_time=stop_time,
    )
    assert sw.start_date == start_date
    assert sw.start_time == start_time
    assert sw.stop_date == stop_date
    assert sw.stop_time == stop_time


def test_send_window_default_values() -> None:
    """SendWindow fields should default to None."""
    sw = SendWindow()
    assert sw.start_date is None
    assert sw.start_time is None
    assert sw.stop_date is None
    assert sw.stop_time is None


def test_send_window_serialize_writes_fields() -> None:
    """SendWindow.serialize writes startDate, startTime, stopDate, stopTime."""
    sw = SendWindow(
        start_date="2024-01-15",
        start_time="08:00:00",
        stop_date="2024-01-16",
        stop_time="20:00:00",
    )
    writer = MagicMock()
    sw.serialize(writer)

    writer.write_str_value.assert_any_call("startDate", "2024-01-15")
    writer.write_str_value.assert_any_call("startTime", "08:00:00")
    writer.write_str_value.assert_any_call("stopDate", "2024-01-16")
    writer.write_str_value.assert_any_call("stopTime", "20:00:00")


def test_send_window_serialize_raises_on_none_writer() -> None:
    """SendWindow.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        SendWindow().serialize(None)  # type: ignore[arg-type]


def test_send_window_deserializer_keys() -> None:
    """SendWindow deserializer keys should be camelCase."""
    keys = set(SendWindow().get_field_deserializers().keys())
    assert keys == {"startDate", "startTime", "stopDate", "stopTime"}


# ---------------------------------------------------------------------------
# Parameter
# ---------------------------------------------------------------------------


def test_parameter_default_values() -> None:
    """Parameter fields should default to None."""
    p = Parameter()
    assert p.key is None
    assert p.value is None


def test_parameter_field_assignment() -> None:
    """Parameter should store key and value correctly."""
    p = Parameter(key="myKey", value="myValue")
    assert p.key == "myKey"
    assert p.value == "myValue"


def test_parameter_serialize_writes_fields() -> None:
    """Parameter.serialize writes key and value."""
    p = Parameter(key="myKey", value="myValue")
    writer = MagicMock()
    p.serialize(writer)

    writer.write_str_value.assert_any_call("key", "myKey")
    writer.write_str_value.assert_any_call("value", "myValue")


def test_parameter_serialize_raises_on_none_writer() -> None:
    """Parameter.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        Parameter().serialize(None)  # type: ignore[arg-type]


def test_parameter_deserializer_keys() -> None:
    """Parameter deserializer should contain 'key' and 'value'."""
    keys = set(Parameter().get_field_deserializers().keys())
    assert keys == {"key", "value"}


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------


def test_settings_default_values() -> None:
    """Settings fields should default to None."""
    s = Settings()
    assert s.age is None
    assert s.auto_detect_encoding is None
    assert s.differentiator is None
    assert s.gas_settings is None
    assert s.invoice_node is None
    assert s.new_session is None
    assert s.originator_settings is None
    assert s.parameter is None
    assert s.priority is None
    assert s.send_window is None
    assert s.session_id is None
    assert s.validity is None


def test_settings_field_assignment(
    originator_settings: OriginatorSettings,
    gas_settings: GasSettings,
    send_window: SendWindow,
    parameter: Parameter,
) -> None:
    """Settings should store all fields correctly."""
    s = Settings(
        age=18,
        auto_detect_encoding=True,
        differentiator="diff-001",
        gas_settings=gas_settings,
        invoice_node="inv-001",
        new_session=False,
        originator_settings=originator_settings,
        parameter=[parameter],
        priority=2,
        send_window=send_window,
        session_id="sess-001",
        validity=60,
    )
    assert s.age == 18
    assert s.auto_detect_encoding is True
    assert s.differentiator == "diff-001"
    assert s.gas_settings is gas_settings
    assert s.invoice_node == "inv-001"
    assert s.new_session is False
    assert s.originator_settings is originator_settings
    assert s.parameter == [parameter]
    assert s.priority == 2
    assert s.send_window is send_window
    assert s.session_id == "sess-001"
    assert s.validity == 60


def test_settings_serialize_raises_on_none_writer() -> None:
    """Settings.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        Settings().serialize(None)  # type: ignore[arg-type]


def test_settings_serialize_writes_fields() -> None:
    """Settings.serialize writes all fields to the writer."""
    s = Settings(priority=1, validity=120, auto_detect_encoding=True)
    writer = MagicMock()
    s.serialize(writer)

    writer.write_int_value.assert_any_call("priority", 1)
    writer.write_int_value.assert_any_call("validity", 120)
    writer.write_bool_value.assert_any_call("autoDetectEncoding", True)


def test_settings_deserializer_keys() -> None:
    """Settings deserializer keys should cover all camelCase fields."""
    keys = set(Settings().get_field_deserializers().keys())
    expected = {
        "age",
        "autoDetectEncoding",
        "differentiator",
        "gasSettings",
        "invoiceNode",
        "newSession",
        "originatorSettings",
        "parameter",
        "priority",
        "sendWindow",
        "sessionId",
        "validity",
    }
    assert keys == expected


# ---------------------------------------------------------------------------
# GatewayRequest
# ---------------------------------------------------------------------------


def test_gateway_request_default_values() -> None:
    """GatewayRequest fields should default to None."""
    req = GatewayRequest()
    assert req.service_id is None
    assert req.username is None
    assert req.password is None
    assert req.batch_reference is None
    assert req.message is None


def test_gateway_request_field_assignment(basic_message: Message) -> None:
    """GatewayRequest should store all fields correctly."""
    req = GatewayRequest(
        service_id=12345,
        username="user",
        password="pass",
        batch_reference="batch-001",
        message=[basic_message],
    )
    assert req.service_id == 12345
    assert req.username == "user"
    assert req.password == "pass"
    assert req.batch_reference == "batch-001"
    assert req.message == [basic_message]


def test_gateway_request_create_from_discriminator_value_raises_on_none() -> None:
    """create_from_discriminator_value raises TypeError when parse_node is None."""
    with pytest.raises(TypeError):
        GatewayRequest.create_from_discriminator_value(None)  # type: ignore[arg-type]


def test_gateway_request_serialize_raises_on_none_writer() -> None:
    """GatewayRequest.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        GatewayRequest().serialize(None)  # type: ignore[arg-type]


def test_gateway_request_serialize_writes_fields(
    basic_message: Message,
) -> None:
    """GatewayRequest.serialize writes all fields to the writer."""
    req = GatewayRequest(
        service_id=12345,
        username="user",
        password="pass",
        batch_reference="batch-001",
        message=[basic_message],
    )
    writer = MagicMock()
    req.serialize(writer)

    writer.write_str_value.assert_any_call("batchReference", "batch-001")
    writer.write_str_value.assert_any_call("password", "pass")
    writer.write_int_value.assert_any_call("serviceId", 12345)
    writer.write_str_value.assert_any_call("username", "user")
    writer.write_collection_of_object_values.assert_called_once_with(
        "message", [basic_message]
    )


def test_gateway_request_deserializer_keys() -> None:
    """GatewayRequest deserializer keys should cover all camelCase fields."""
    keys = set(GatewayRequest().get_field_deserializers().keys())
    assert keys == {
        "batchReference",
        "message",
        "password",
        "serviceId",
        "username",
    }


# ---------------------------------------------------------------------------
# GatewayResponse
# ---------------------------------------------------------------------------


def test_gateway_response_default_values() -> None:
    """GatewayResponse fields should default to None."""
    resp = GatewayResponse()
    assert resp.batch_reference is None
    assert resp.message_status is None


def test_gateway_response_field_assignment(
    message_status: MessageStatus,
) -> None:
    """GatewayResponse should store batch_reference and message_status."""
    resp = GatewayResponse(
        batch_reference="batch-001",
        message_status=[message_status],
    )
    assert resp.batch_reference == "batch-001"
    assert resp.message_status == [message_status]


def test_gateway_response_serialize_writes_fields(
    message_status: MessageStatus,
) -> None:
    """GatewayResponse.serialize writes batchReference and messageStatus."""
    resp = GatewayResponse(
        batch_reference="batch-001",
        message_status=[message_status],
    )
    writer = MagicMock()
    resp.serialize(writer)

    writer.write_str_value.assert_called_once_with(
        "batchReference", "batch-001"
    )
    writer.write_collection_of_object_values.assert_called_once_with(
        "messageStatus", [message_status]
    )


def test_gateway_response_deserializer_keys() -> None:
    """GatewayResponse deserializer keys should be camelCase."""
    keys = set(GatewayResponse().get_field_deserializers().keys())
    assert keys == {"batchReference", "messageStatus"}


# ---------------------------------------------------------------------------
# MessageStatus
# ---------------------------------------------------------------------------


def test_message_status_default_values() -> None:
    """MessageStatus fields should default to None."""
    ms = MessageStatus()
    assert ms.message_id is None
    assert ms.recipient is None
    assert ms.status_code is None
    assert ms.status_message is None
    assert ms.sequence_index is None
    assert ms.client_reference is None
    assert ms.session_id is None


def test_message_status_field_assignment() -> None:
    """MessageStatus should store all fields correctly."""
    ms = MessageStatus(
        message_id="msg-001",
        recipient="+4799999999",
        status_code=200,
        status_message="OK",
        sequence_index=1,
        client_reference="ref-001",
        session_id="sess-001",
    )
    assert ms.message_id == "msg-001"
    assert ms.recipient == "+4799999999"
    assert ms.status_code == 200
    assert ms.status_message == "OK"
    assert ms.sequence_index == 1
    assert ms.client_reference == "ref-001"
    assert ms.session_id == "sess-001"


def test_message_status_serialize_writes_fields() -> None:
    """MessageStatus.serialize writes all fields to the writer."""
    ms = MessageStatus(
        message_id="msg-001",
        recipient="+4799999999",
        status_code=200,
        status_message="OK",
        sequence_index=1,
    )
    writer = MagicMock()
    ms.serialize(writer)

    writer.write_str_value.assert_any_call("messageId", "msg-001")
    writer.write_str_value.assert_any_call("recipient", "+4799999999")
    writer.write_int_value.assert_any_call("statusCode", 200)
    writer.write_str_value.assert_any_call("statusMessage", "OK")
    writer.write_int_value.assert_any_call("sequenceIndex", 1)


def test_message_status_deserializer_keys() -> None:
    """MessageStatus deserializer keys should cover all camelCase fields."""
    keys = set(MessageStatus().get_field_deserializers().keys())
    assert keys == {
        "clientReference",
        "messageId",
        "recipient",
        "sequenceIndex",
        "sessionId",
        "statusCode",
        "statusMessage",
    }


def test_message_status_serialize_raises_on_none_writer() -> None:
    """MessageStatus.serialize raises TypeError when writer is None."""
    with pytest.raises(TypeError, match="writer cannot be null"):
        MessageStatus().serialize(None)  # type: ignore[arg-type]
