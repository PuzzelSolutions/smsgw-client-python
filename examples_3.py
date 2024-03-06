"""Example of how to use the library by using the object instances."""

from puzzel_sms_gateway_client import (
    Client,
    GasSettings,
    Message,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
)


BASE_ADDRESS = "NEEDS TO BE SET BY THE USER"
SERVICE_ID = 0000  # NEEDS TO BE SET BY THE USER
USERNAME = "NEEDS TO BE SET BY THE USER"
PASSWORD = "NEEDS TO BE SET BY THE USER"
RECIPIENT = "+4710101010"

gas_settings = GasSettings(
    service_code="02001",
    description="SMS",  # Optional
)

originator_settings = OriginatorSettings(
    originator_type="NETWORK",
    originator="1960",
)

send_window = SendWindow(
    start_date="2023-04-26",
    stop_date="2023-04-26",  # Optional # If not included SMS is sent immediately
    start_time="22:20:00",
    stop_time="22:30:00",  # Optional # If not included SMS is sent immediately
)

parameter = Parameter(  # All are optional
    business_model="contact center",
    dcs="F5",
    udh="0B0504158200000023AB0201",
    pid=65,
    flash=True,
    parsing_type="AUTO_DETECT",
    skip_customer_report_delivery=True,
    strex_verification_timeout="10",
    strex_merchant_sell_option="pin",
    strex_confirm_channel="sms",
    strex_authorization_token="some_token",
)

message_settings = MessageSettings(  # All are optional
    priority=1,
    validity=173,
    differentiator="sms group 1",
    invoice_node="marketing department",
    age=18,
    new_session=True,
    session_id="01bxmt7f8b8h3zkwe2vg",
    auto_detect_encoding=True,
    safe_remove_non_gsm_characters=True,  # Deprecated
    originator_settings=originator_settings,
    gas_settings=gas_settings,
    send_window=send_window,
    parameter=parameter,
)


client = Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
    batch_reference="some_batch_reference",  # Optional
)

message = Message(
    recipient=RECIPIENT,
    content="Hello World!",
    price=100,  # Optional
    client_reference="some_client_reference",  # Optional
    settings=message_settings,  # Optional
)

client.send(messages=[message])
