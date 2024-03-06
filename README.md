# Puzzel SMS Gateway Python Client <!-- omit in toc -->

[![GitHub License](https://img.shields.io/github/license/PuzzelSolutions/puzzel_smsgw?color=blue)](LICENSE)
[![Latest Version](https://img.shields.io/pypi/v/puzzel_smsgw.svg)](https://pypi.python.org/pypi/puzzel_smsgw/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/puzzel_smsgw.svg)](https://pypi.python.org/pypi/puzzel_smsgw/)
[![Downloads](https://pepy.tech/badge/puzzel_smsgw)](https://pepy.tech/project/puzzel_smsgw)
[![Coverage](https://img.shields.io/codecov/c/github/PuzzelSolutions/puzzel_smsgw?color=blue)](https://app.codecov.io/gh/PuzzelSolutions/puzzel_smsgw)
[![GitHub issues](https://img.shields.io/github/issues-raw/PuzzelSolutions/puzzel_smsgw)](https://github.com/PuzzelSolutions/puzzel_smsgw/issues)
![GitHub last commit](https://img.shields.io/github/last-commit/PuzzelSolutions/puzzel_smsgw)

Copyright 2024 [Puzzel AS](https://www.puzzel.com)\
[_Released under the MIT license_](LICENSE).

Python client for the Puzzel SMS Gateway.

## Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Using Poetry](#using-poetry)
- [Usage](#usage)
  - [Importing as a module](#importing-as-a-module)
  - [Using classes directly](#using-classes-directly)
  - [Using object instantiation](#using-object-instantiation)
  - [Sending message to multiple recipients](#sending-message-to-multiple-recipients)

## Prerequisites

```toml
python = "^3.10.5"
requests = "^2.28.1"
pydantic = "^1.9.1"
fastapi = "^0.78.0"
```

Please see [pyproject.toml](pyproject.toml) for the full citation information.

## Installation

### Using pip

```bash
python -m pip install puzzel_sms_gateway_client
```

### Using Poetry

```bash
poetry add puzzel_sms_gateway_client
```

## Usage

For all the following examples it is recommended to define the following needed variables as secrets in your repository, environment variables or as constants in the script.

### Importing as a module

```python
import puzzel_sms_gateway_client as smsgw

BASE_ADDRESS: str = "https://[YOUR_SERVER_ADDRESS]/gw/rs"
SERVICE_ID: int = [YOUR_SERVICE_ID]
USERNAME: str = "[YOUR_USERNAME]"
PASSWORD: str = "[YOUR_PASSWORD]"


client = smsgw.Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)

response = client.send(
    messages=[
        smsgw.Message(
            recipient="+47xxxxxxxxx",  # Country code + phone number
            content="Hello World!",
        ),
    ]
)
```

### Using classes directly

```python
from puzzel_sms_gateway_client import (
    Client,
    GasSettings,
    Message,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
)


BASE_ADDRESS: str = "https://[YOUR_SERVER_ADDRESS]/gw/rs"
SERVICE_ID: int = [YOUR_SERVICE_ID]
USERNAME: str = "[YOUR_USERNAME]"
PASSWORD: str = "[YOUR_PASSWORD]"


client = Client(
    service_id=SERVICE_ID,
    username=USERNAME,
    password=PASSWORD,
    base_address=BASE_ADDRESS,
)

response = client.send(
    messages=[
        Message(
            recipient="+47xxxxxxxxx",  # Country code + phone number
            content="Hello World!",
            settings=MessageSettings(  # Optional
                send_window=SendWindow(
                    start_date="2022-07-13",
                    stop_date="2022-07-13", # Optional
                    start_time="15:20:00",
                    stop_time="15:30:00", # Optional
                ),
            ),
        ),
    ]
)
```

### Using object instantiation

```python
from puzzel_sms_gateway_client import (
    Client,
    GasSettings,
    Message,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
)

BASE_ADDRESS: str = "https://[YOUR_SERVER_ADDRESS]/gw/rs"
SERVICE_ID: int = [YOUR_SERVICE_ID]
USERNAME: str = "[YOUR_USERNAME]"
PASSWORD: str = "[YOUR_PASSWORD]"

gas_settings = GasSettings(
    service_code="02001",
    description="SMS",  # Optional
)

originator_settings = OriginatorSettings(
    originator_type="NETWORK",
    originator="1960",
)

send_window = SendWindow(
    start_date="2022-07-14",
    stop_date="2022-07-14",  # Optional
    start_time="09:20:00",
    stop_time="09:30:00",  # Optional
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
    recipient="+47xxxxxxxxx",  # Country code + phone number
    content="Hello World!",
    price=100,  # Optional
    client_reference="some_client_reference",  # Optional
    settings=message_settings,  # Optional
)

response = client.send(messages=[message])
```

### Sending message to multiple recipients

```python
import json

from puzzel_sms_gateway_client import (
    Client,
    Message,
)

BASE_ADDRESS: str = "https://[YOUR_SERVER_ADDRESS]/gw/rs"
SERVICE_ID: int = [YOUR_SERVICE_ID]
USERNAME: str = "[YOUR_USERNAME]"
PASSWORD: str = "[YOUR_PASSWORD]"

recipients = [
    "+47xxxxxxxx1",  # Country code + phone number
    "+47xxxxxxxx2",  # Country code + phone number
]


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

print(json.dumps(response.json(), indent=4))
```

Output:

```json
{
  "batchReference": "60908fdd-6da7-4658-b0f7-5685e513c19f",
  "messageStatus": [
    {
      "statusCode": 1,
      "statusMessage": "Message enqueued for sending",
      "clientReference": null,
      "recipient": "+47xxxxxxxx1",
      "messageId": "7a04egxihb00",
      "sessionId": null,
      "sequenceIndex": 1
    },
    {
      "statusCode": 1,
      "statusMessage": "Message enqueued for sending",
      "clientReference": null,
      "recipient": "+47xxxxxxxx2",
      "messageId": "7a04egxihc00",
      "sessionId": null,
      "sequenceIndex": 2
    }
  ]
}
```
