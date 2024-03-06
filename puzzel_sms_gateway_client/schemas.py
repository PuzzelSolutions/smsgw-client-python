"""Data schemas for the puzzel_smsgw application."""

import datetime
import json
from typing import Literal
from warnings import warn

from pydantic import BaseModel, validator

from puzzel_sms_gateway_client import _exceptions

# Date in format YYYY-MM-DD.
DATE_FMT = "%Y-%m-%d"
# Time in format hh:mm:ss.
TIME_FMT = "%H:%M:%S"


class OriginatorSettings(BaseModel):
    """Data schema for the originator settings object."""

    originator_type: Literal["INTERNATIONAL", "ALPHANUMERIC", "NETWORK"]
    originator: str


class GasSettings(BaseModel):
    """Data schema for the gas settings object."""

    service_code: str
    description: str = ""


class SendWindow(BaseModel):
    """Data schema for the send window object."""

    start_date: str
    stop_date: str | None = None
    start_time: str
    stop_time: str | None = None

    @validator("start_date", "stop_date")
    def validate_date(cls, v: str) -> str:
        """Validate date format.

        Parameters
        ----------
        v : str
            Date in format YYYY-MM-DD.

        Returns
        -------
        str
            Date in format YYYY-MM-DD.

        Raises
        ------
        _exceptions.InvalidDateFormat
            If the date format is invalid.
        """
        try:
            datetime.datetime.strptime(v, DATE_FMT)
        except ValueError:
            raise _exceptions.InvalidDateFormat(
                f"Invalid date format: {v}\n" f"Expected format: {DATE_FMT}"
            )
        return v

    @validator("start_time", "stop_time")
    def validate_time(cls, v: str) -> str:
        """Validate time format.

        Parameters
        ----------
        v : str
            Time in format hh:mm:ss.

        Returns
        -------
        str
            Time in format hh:mm:ss.

        Raises
        ------
        _exceptions.InvalidTimeFormat
            If the time format is invalid.
        """
        try:
            datetime.datetime.strptime(v, TIME_FMT)
        except ValueError:
            raise _exceptions.InvalidTimeFormat(
                f"Invalid time format: {v}\n" f"Expected format: {TIME_FMT}"
            )
        return v


class Parameter(BaseModel):
    """Data schema for the parameter object."""

    business_model: str | None = None
    dcs: str | None = None
    udh: str | None = None
    pid: int | None = None
    flash: bool | None = None
    parsing_type: (
        Literal[
            "NONE",
            "SAFE_REMOVE_NON_GSM",
            "SAFE_REMOVE_NON_GSM_WITH_REPLACE",
            "AUTO_DETECT",
        ]
        | None
    ) = None
    skip_customer_report_delivery: bool | None = None
    strex_verification_timeout: str | None = None
    strex_merchant_sell_option: (
        Literal["none", "confirmation", "pin"] | None
    ) = None
    strex_confirm_channel: Literal["sms", "ussd", "otp"] | None = None
    strex_authorization_token: str | None = None

    @validator("dcs")
    def validate_dcs(cls, v: str) -> str:
        """Validate dcs.

        Parameters
        ----------
        v : str
            Should be one octet (2 hex digits). For example '15' or 'F5'.

        Returns
        -------
        str
            Value of dcs.

        Raises
        ------
        _exceptions.InvalidDcs
            If the dcs is invalid.
        """
        if v is not None and len(v) != 2 and int(v, 16):
            raise _exceptions.InvalidDcs(
                f"Invalid dcs: {v}\n" f"Expected format: 15 or F5"
            )
        return v

    @validator("udh")
    def validate_udh(cls, v: str) -> str:
        """Validate udh.

        Parameters
        ----------
        v : str
            Should be one or more octets. For example '0B' or '0BFF'.

        Returns
        -------
        str
            Value of udh.

        Raises
        ------
        _exceptions.InvalidUdh
            If the udh is invalid.
        """
        if v is not None and len(v) % 2 != 0 and int(v, 16):
            raise _exceptions.InvalidUdh(
                f"Invalid udh: {v}\n" f"Expected format: 0BFF0BF0"
            )
        return v

    @validator("pid")
    def validate_pid(cls, v: int) -> int:
        """Validate pid.

        Parameters
        ----------
        v : int
            Should be in the range 65 to 71

        Returns
        -------
        int
            Value of pid.

        Raises
        ------
        _exceptions.InvalidPid
            If the pid is invalid.
        """
        if v is not None and v < 65 or v > 71:
            raise _exceptions.InvalidPid(
                f"Invalid pid: {v}\n" f"Expected range: 65-71"
            )
        return v

    @validator("strex_verification_timeout")
    def validate_strex_verification_timeout(cls, v: str) -> str:
        """Validate strex_verification_timeout.

        Parameters
        ----------
        v : str
            Should be in the range 0 to 30.

        Returns
        -------
        str
            Value of strex_verification_timeout.

        Raises
        ------
        _exceptions.InvalidStrexVerificationTimeout
            If the strex_verification_timeout is invalid.
        """
        if v is not None and int(v) < 0 or int(v) > 31:
            raise _exceptions.InvalidStrexVerificationTimeout(
                f"Invalid strex_verification_timeout: {v}\n"
                f"Expected range: 0-30"
            )
        return v

    @validator("strex_confirm_channel")
    def validate_strex_confirm_channel(cls, v: str) -> str:
        """Validate strex_confirm_channel.

        Parameters
        ----------
        v : str
            Should be one octet (2 hex digits). For example '15' or 'F5'.

        Returns
        -------
        str
            Value of strex_confirm_channel.

        Raises
        ------
        _exceptions.InvalidStrexConfirmChannel
            If the strex_confirm_channel is invalid.
        _exceptions.InvalidStrexConfirmChannel
            If the strex_confirm_channel is invalid.
        """
        if v is not None and v not in ["sms", "ussd", "otp"]:
            raise _exceptions.InvalidStrexConfirmChannel(
                f"Invalid strex_confirm_channel: {v}\n"
                f"Expected values: sms, ussd, otp"
            )
        elif v == "ussd":
            warn(
                message="strex_confirm_channel=ussd is deprecated. ",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return v
        elif v == "otp":
            raise _exceptions.InvalidStrexConfirmChannel(
                f"Invalid strex_confirm_channel: {v}\n" f"{v} is not in use"
            )
        return v

    @staticmethod
    def _k_v_format(key: str, value: str | int | bool) -> dict:
        """Format key-value pair to the format expected by the SMS Gateway.

        Parameters
        ----------
        key : str
            Key.
        value : str | int | bool
            Value.

        Returns
        -------
        dict
            Key-value pair in the format expected by the SMS Gateway.
        """
        return {
            "key": key,
            "value": value,
        }

    def list(self) -> list[dict]:
        """Format parameter object to the format expected by the SMS Gateway.

        Returns
        -------
        list[dict]
            List of key-value pairs in the format expected by the SMS Gateway.
        """
        return [
            self._k_v_format(key, value)
            for key, value in self.dict().items()
            if value is not None
        ]

    def __str__(self) -> str:
        """Format parameter object to the format expected by the SMS Gateway.

        Returns
        -------
        str
            String representation of the parameter object.
        """
        k_v_list = self.list()
        return json.dumps(k_v_list, indent=4)


class MessageSettings(BaseModel):
    """Data schema for the message settings object."""

    priority: Literal[1, 2, 3] | None = None
    validity: int | None = None
    differentiator: str | None = None
    invoice_node: str | None = None
    age: Literal[0, 16, 18] | None = None
    new_session: bool | None = None
    session_id: str | None = None
    auto_detect_encoding: bool | None = None
    safe_remove_non_gsm_characters: bool | None = None
    originator_settings: OriginatorSettings | None = None
    gas_settings: GasSettings | None = None
    send_window: SendWindow | None = None
    parameter: list[dict[str, str | int | bool]] | Parameter | None = None

    @validator("safe_remove_non_gsm_characters")
    def safe_remove_non_gsm_characters_deprecated(
        cls, v: bool | None
    ) -> bool | None:
        """Warn deprecated safe_remove_non_gsm_characters.

        Parameters
        ----------
        v : bool | None
            Value of safe_remove_non_gsm_characters.

        Returns
        -------
        bool | None
            Value of safe_remove_non_gsm_characters.

        Raises
        ------
        _exceptions.DeprecatedFeature
            If safe_remove_non_gsm_characters is used.
        """
        if v is not None:
            warn(
                message=(
                    "safe_remove_non_gsm_characters is deprecated "
                    "and will be removed in the next version."
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
        return v

    @validator("parameter")
    def parameter_list(
        cls, v: list[dict[str, str | int | bool]] | Parameter | None
    ) -> list[dict]:
        """Format parameter object to the format expected by the SMS Gateway.

        Parameters
        ----------
        v : list[dict] | Parameter | None
            Value of parameter.

        Returns
        -------
        list[dict]
            List of key-value pairs in the format expected by the SMS Gateway.

        Raises
        ------
        _exceptions.InvalidParameter
            If the parameter is invalid.
        """
        if isinstance(v, Parameter):
            return v.list()
        elif isinstance(v, list):
            return v
        else:
            raise _exceptions.InvalidParameter(
                f"Invalid parameter: {v}\n" f"Expected type: Parameter"
            )


class Message(BaseModel):
    """Data schema for the message object."""

    recipient: str = "Must be defined before sending"
    content: str
    price: int | None = None
    client_reference: str | None = None
    settings: MessageSettings | None = None

    @validator("recipient")
    def validate_msisdn(cls, v: str) -> str:
        """Validate MSISDN format.

        Parameters
        ----------
        v : str
            MSISDN.

        Returns
        -------
        str
            MSISDN.

        Raises
        ------
        _exceptions.InvalidMsisdnFormat
            If the MSISDN is not in the correct format.
        """
        if v == "Must be defined before sending":
            return v

        if not v.startswith("+") or not v.replace("+", "").isdigit():
            raise _exceptions.InvalidMsisdnFormat(
                f"Invalid MSISDN format: {v}\n" f"Expected format: +123456789"
            )
        return v

    def __str__(self) -> str:
        """Format message object to the format expected by the SMS Gateway.

        Returns
        -------
        str
            String representation of the message object.
        """
        return json.dumps(self.dict(), indent=4)


class _Request(BaseModel):
    """Data schema for the request object."""

    service_id: int
    username: str
    password: str
    message: list[Message]
    batch_reference: str | None = None

    @staticmethod
    def _to_camel(string: str) -> str:
        """Convert string to camel case.

        Parameters
        ----------
        string : str
            String to convert.

        Returns
        -------
        str
            String in camel case.
        """
        if "_" in string:
            words = string.split("_")
            return "".join(
                [words[0].lower()] + [word.capitalize() for word in words[1:]]
            )
        return string

    @staticmethod
    def _to_camel_dict_recursive(d: dict) -> dict:
        """Convert dictionary keys to camel case.

        Also supports nested dictionaries and lists of dictionaries.

        Parameters
        ----------
        d : dict
            Dictionary to convert.

        Returns
        -------
        dict
            Dictionary in camel case.
        """
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = _Request._to_camel_dict_recursive(v)
            elif isinstance(v, list):
                d[k] = [_Request._to_camel_dict_recursive(item) for item in v]
        return {_Request._to_camel(k): v for k, v in d.items()}

    def dict(self, camel_case=False, *args, **kwargs):
        """Convert request to dictionary.

        Parameters
        ----------
        camel_case : bool
            If True, convert keys to camel case.
            Defaults to False.

        Returns
        -------
        dict
            Request as dictionary.
        """
        if camel_case:
            return _Request._to_camel_dict_recursive(
                self.dict(*args, **kwargs)
            )
        return super().dict(*args, **kwargs)
