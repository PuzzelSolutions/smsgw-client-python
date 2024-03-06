"""Example of how to use the library by using the classes directly."""

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


client = Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)

client.send(
    messages=[
        Message(
            recipient=RECIPIENT,
            content="Hello World!",
            settings=MessageSettings(  # Optional
                send_window=SendWindow(
                    start_date="2023-04-26",
                    stop_date="2022-04-26",  # Optional # If not included SMS is sent immediately
                    start_time="22:15:00",
                    stop_time="22:16:00",  # Optional # If not included SMS is sent immediately
                ),
            ),
        ),
    ]
)
