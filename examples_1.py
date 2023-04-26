"""Examples of how to use the library by importing the library as a module."""
import puzzel_sms_gateway_client as smsgw


base_address = "https://smsgw.puzzel.com/gw/rs"  # TODO: Mask this
service_id = 2238  # TODO: Mask this
username = "kjapptest"  # TODO: Mask this
password = "kjapptest"  # TODO: Mask this
recipient = "+4795002946"  # TODO: Mask this


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
