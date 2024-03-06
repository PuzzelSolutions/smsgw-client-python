"""Example of how to use the library by using the classes directly"""

from puzzel_sms_gateway_client import (
    Client,
    GasSettings,
    Message,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
)


BASE_ADDRESS = "https://smsgw.puzzel.com/gw/rs"  # TODO: Mask this
SERVICE_ID = 2238  # TODO: Mask this
USERNAME = "kjapptest"  # TODO: Mask this
PASSWORD = "kjapptest"  # TODO: Mask this

recipient = "+4795002946"  # TODO: Mask this


client = Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)

client.send(
    messages=[
        Message(
            recipient=recipient,
            content="Hello World!",
            settings=MessageSettings(  # Optional
                send_window=SendWindow(
                    start_date="2023-04-26",
                    stop_date="2022-04-26",  # Optional # TODO: If not included SMS is sent immediately
                    start_time="22:15:00",
                    stop_time="22:16:00",  # Optional # TODO: If not included SMS is sent immediately
                ),
            ),
        ),
    ]
)
