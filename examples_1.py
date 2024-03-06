"""Examples of how to use the library by importing the library as a module."""

import puzzel_sms_gateway_client as smsgw

base_address = "NEEDS TO BE SET BY THE USER"
service_id = 0000  # NEEDS TO BE SET BY THE USER
username = "NEEDS TO BE SET BY THE USER"
password = "NEEDS TO BE SET BY THE USER"
recipient = "+4710101010"


client = smsgw.Client(
    service_id=service_id,
    username=username,
    password=password,
    base_address=base_address,
)

client.send(
    messages=[
        smsgw.Message(
            recipient=recipient,
            content="Hello World!",
        ),
    ]
)
