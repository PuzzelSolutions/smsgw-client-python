"""Example of how to send a message to multiple recipients."""
import json

from puzzel_sms_gateway_client import Client, Message


BASE_ADDRESS = "https://smsgw.puzzel.com/gw/rs"  # TODO: Mask this
SERVICE_ID = 2238  # TODO: Mask this
USERNAME = "kjapptest"  # TODO: Mask this
PASSWORD = "kjapptest"  # TODO: Mask this

recipients = ["+4795002946", "+4795002946"]  # TODO: Mask this

client = Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)

response = client.send(
    messages=[
        Message(
            content="Hello World!",
        )
    ],
    recipients=recipients,
)
# pretty print response
print("\n")
print(json.dumps(response.json(), indent=4))
