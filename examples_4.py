"""Example of how to send a message to multiple recipients."""

import json

from puzzel_sms_gateway_client import Client, Message

BASE_ADDRESS = "NEEDS TO BE SET BY THE USER"
SERVICE_ID = 0000  # NEEDS TO BE SET BY THE USER
USERNAME = "NEEDS TO BE SET BY THE USER"
PASSWORD = "NEEDS TO BE SET BY THE USER"

RECIPIENTS = ["+4710101010", "+4712121212"]

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
    recipients=RECIPIENTS,
)
# pretty print response
print("\n")
print(json.dumps(response.json(), indent=4))
