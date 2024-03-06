"""Python client for Puzzel SMS Gateway."""

import json

import requests
from fastapi import status
from puzzel_sms_gateway_client import Message, _exceptions, _Request
from requests import Response


class Client:
    """Python client for Puzzel SMS Gateway."""

    SEND_MESSAGES_ENDPOINT: str = "/sendMessages"
    HEADERS: dict[str, str] = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }

    def __init__(
        self,
        *,
        service_id: int,
        username: str,
        password: str,
        base_address: str,
        batch_reference: str | None = None,
    ):
        """
        Initialize the client.

        Parameters
        ----------
        service_id : int
            Service ID.
        username : str
            Username.
        password : str
            Password.
        base_address : str
            Base address of the SMS Gateway.
        batch_reference : str | None, optional
            Batch reference. Defaults to None.
        """
        self.base_address = base_address
        self.service_id = service_id
        self.username = username
        self.password = password
        self.batch_reference = batch_reference
        self.send_messages_url = (
            f"{self.base_address}{Client.SEND_MESSAGES_ENDPOINT}"
        )

    def send(
        self, messages: list[Message], recipients: list[str] | None = None
    ):
        """
        Send messages.

        Parameters
        ----------
        messages : list[Message]
            Messages to send.
        recipients : list[str] | None, optional
            Recipients (Will overwrite messages.recipient). Defaults to None.

        Returns
        -------
        Response
            Response from the SMS Gateway.

        Raises
        ------
        _exceptions.MissingMessages
            If no messages are provided.
        _exceptions.GatewayRequestError
            If the request to the SMS Gateway fails.
        """
        request: _Request = _Request(
            service_id=self.service_id,
            username=self.username,
            password=self.password,
            batch_reference=self.batch_reference,
            message=[],
        )

        if len(messages) == 0:
            raise _exceptions.MissingMessages(
                "No messages to send. Please provide at least one message."
            )

        if recipients:
            for recipient in recipients:
                msg = messages[0].copy()
                msg.recipient = recipient
                request.message.append(msg)
        else:
            for message in messages:
                if message.recipient == "Must be defined before sending":
                    raise _exceptions.MissingRecipient(
                        "Recipient must be defined before sending."
                    )
                request.message.append(message)

        data: str = json.dumps(request.dict(camel_case=True))

        # The gateway expects to receive the parameter key 'parsing_type' in
        # the form of 'parsing-type'. Hyphenated naming is not allowed in
        # python, and needs to be converted.
        if "parsing_type" in data:
            data = data.replace("parsing_type", "parsing-type")

        response: Response = requests.post(
            self.send_messages_url, data=data, headers=Client.HEADERS
        )

        if response.status_code != status.HTTP_200_OK:
            raise _exceptions.GatewayRequestError(
                f"Error sending messages. "
                f"Response status code: {response.status_code}"
            )

        return response
