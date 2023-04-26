"""Test the data models for the SMS Gateway."""

import datetime
import random

import pytest
from puzzel_sms_gateway_client import (
    GasSettings,
    MessageSettings,
    OriginatorSettings,
    Parameter,
    SendWindow,
    _exceptions,
)
from puzzel_sms_gateway_client.schemas import DATE_FMT, TIME_FMT
from pydantic.error_wrappers import ValidationError


@pytest.mark.parametrize(
    "originator_type,originator",
    [
        ("INTERNATIONAL", "+4799999999"),
        ("ALPHANUMERIC", "Puzzel"),
        ("NETWORK", "1960"),
    ],
)
def test_originator_settings_should_pass(originator_type, originator):
    """Test the originator settings."""
    originator_settings = OriginatorSettings(
        originator_type=originator_type,
        originator=originator,
    )

    assert originator_settings.originator_type == originator_type
    assert type(originator_settings.originator_type) is str
    assert originator_settings.originator_type != ""
    assert originator_settings.originator_type is not None

    assert originator_settings.originator == originator
    assert type(originator_settings.originator) is str
    assert originator_settings.originator != ""
    assert originator_settings.originator is not None


@pytest.mark.xfail(reason="Missing mandatory parameter")
def test_originator_settings_should_fail():
    """Test the originator settings."""
    originator_settings = OriginatorSettings()  # type: ignore


def test_gas_settings_should_pass():
    """Test the gas settings."""
    SERVICE_CODE: str = "01010"
    DESCRIPTION: str = "Test"
    SERVICE_CODE_LENGTH: int = 5

    gas_settings = GasSettings(
        service_code=SERVICE_CODE,
        description=DESCRIPTION,
    )

    assert gas_settings.service_code == SERVICE_CODE
    assert type(gas_settings.service_code) is str
    assert gas_settings.service_code != ""
    assert gas_settings.service_code is not None
    assert len(gas_settings.service_code) == SERVICE_CODE_LENGTH

    assert gas_settings.description == DESCRIPTION
    assert type(gas_settings.description) is str
    assert gas_settings.description != ""
    assert gas_settings.description is not None


@pytest.mark.xfail(reason="Missing mandatory parameter")
def test_gas_settings_should_fail():
    """Test the gas settings."""
    gas_settings = GasSettings()  # type: ignore


@pytest.mark.parametrize(
    "start_date,stop_date,start_time,stop_time",
    [
        (
            datetime.datetime.now().strftime(DATE_FMT),
            (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                DATE_FMT
            ),
            datetime.datetime.now().strftime(TIME_FMT),
            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                TIME_FMT
            ),
        ),
        ("2022-07-15", None, "14:30:00", None),
    ],
)
def test_send_window_all_should_pass(
    start_date, stop_date, start_time, stop_time
):
    """Test the send window with all parameters."""
    if stop_date and stop_time:
        send_window = SendWindow(
            start_date=start_date,
            stop_date=stop_date,
            start_time=start_time,
            stop_time=stop_time,
        )
        assert type(send_window.stop_date) is str
        assert send_window.stop_date is not None

        assert type(send_window.stop_time) is str
        assert send_window.stop_time is not None

    else:
        send_window = SendWindow(
            start_date=start_date,
            start_time=start_time,
        )
        assert send_window.stop_date is None
        assert send_window.stop_time is None

    assert send_window.start_date == start_date
    assert type(send_window.start_date) is str
    assert send_window.start_date != ""
    assert send_window.start_date is not None

    assert send_window.stop_date == stop_date
    assert send_window.stop_date != ""

    assert send_window.start_time == start_time
    assert type(send_window.start_time) is str
    assert send_window.start_time != ""
    assert send_window.start_time is not None

    assert send_window.stop_time == stop_time
    assert send_window.stop_time != ""


@pytest.mark.xfail(reason="Missing mandatory parameter")
def test_send_window_non_should_fail():
    """Test send window with no parameters."""
    send_window = SendWindow()  # type: ignore


@pytest.mark.parametrize(
    "start_date",
    [
        "22.07.15",
        "2022.07.15",
        "15.07.22",
        "15.07.2022",
    ],
)
@pytest.mark.xfail(raises=_exceptions.InvalidDateFormat)
def test_send_window_invalid_date_format_should_fail(start_date):
    """Test the send window with invalid date format."""
    send_window = SendWindow(
        start_date=start_date,
        start_time="14:30:00",
    )


@pytest.mark.parametrize(
    "start_time",
    [
        "14.30.00",
        "14:30",
        "14-30-00",
    ],
)
@pytest.mark.xfail(raises=_exceptions.InvalidTimeFormat)
def test_send_window_invalid_time_format_should_fail(start_time):
    """Test the parameter with invalid time format."""
    parameter = SendWindow(
        start_date="2022-07-15",
        start_time=start_time,
    )


def test_parameter_all_should_pass():
    """Test all parameters."""
    pid = random.randint(65, 71)
    parameter = Parameter(
        business_model="contact center",
        dcs="F5",
        udh="0B0504158200000023AB0201",
        pid=pid,
        flash=True,
        parsing_type="AUTO_DETECT",
        skip_customer_report_delivery=True,
        strex_verification_timeout="10",
        strex_merchant_sell_option="pin",
        strex_confirm_channel="sms",
        strex_authorization_token="some_token",
    )

    assert parameter.business_model == "contact center"
    assert parameter.dcs == "F5"
    assert parameter.udh == "0B0504158200000023AB0201"
    assert parameter.pid == pid
    assert parameter.flash is True
    assert parameter.parsing_type == "AUTO_DETECT"
    assert parameter.skip_customer_report_delivery is True
    assert parameter.strex_verification_timeout == "10"
    assert parameter.strex_merchant_sell_option == "pin"
    assert parameter.strex_confirm_channel == "sms"
    assert parameter.strex_authorization_token == "some_token"

    params = [x for x in parameter.__dict__.keys()]

    for param in params:
        assert parameter.__dict__[param] != ""
        assert parameter.__dict__[param] is not None


def test_parameter_non_should_pass():
    """Test no parameters."""
    parameter = Parameter()  # type: ignore


@pytest.mark.parametrize(
    "dcs",
    [
        "234",
        "F",
        "F5F6g",
    ],
)
@pytest.mark.xfail(raises=(_exceptions.InvalidDcs, ValidationError))
def test_parameter_invalid_dcs_should_fail(dcs):
    """Test the parameter with invalid dcs."""
    with pytest.raises(_exceptions.InvalidDcs):
        Parameter(dcs=dcs)

    # ValidationError
    Parameter(
        dcs=dcs,
    )


@pytest.mark.parametrize(
    "udh",
    [
        "F",
        "F5H",
        "0B0504158200000023AB02010",
    ],
)
@pytest.mark.xfail(raises=(_exceptions.InvalidUdh, ValidationError))
def test_parameter_invalid_udh_should_fail(udh):
    """Test the parameter with invalid udh."""
    with pytest.raises(_exceptions.InvalidUdh):
        Parameter(udh=udh)

    # ValidationError
    Parameter(
        udh=udh,
    )


@pytest.mark.parametrize(
    "pid",
    # random number between 0-64 or 72-255
    [
        random.randint(0, 64),
        random.randint(72, 255),
    ],
)
@pytest.mark.xfail(raises=_exceptions.InvalidPid)
def test_parameter_invalid_pid_should_fail(pid):
    """Test the parameter with invalid pid."""
    parameter = Parameter(pid=pid)


@pytest.mark.parametrize(
    "parsing_type",
    [
        "NONE",
        "SAFE_REMOVE_NON_GSM",
        "SAFE_REMOVE_NON_GSM_WITH_REPLACE",
        "AUTO_DETECT",
    ],
)
def test_parameter_parsing_type_should_pass(parsing_type):
    """Test the parameter parsing type."""
    parameter = Parameter(
        parsing_type=parsing_type,
    )

    assert parameter.parsing_type == parsing_type
    assert type(parameter.parsing_type) is str
    assert parameter.parsing_type != ""
    assert parameter.parsing_type is not None


@pytest.mark.parametrize(
    "strex_verification_timeout",
    ["-1", "31"],
)
@pytest.mark.xfail(raises=_exceptions.InvalidStrexVerificationTimeout)
def test_parameter_invalid_strex_verification_timeout_should_fail(
    strex_verification_timeout,
):
    """Test the parameter with invalid strex verification timeout."""
    parameter = Parameter(
        strex_verification_timeout=strex_verification_timeout,
    )


@pytest.mark.parametrize(
    "strex_sell_option",
    [
        "none",
        "confirmation",
        "pin",
    ],
)
def test_parameter_strex_sell_option_should_pass(strex_sell_option):
    """Test the parameter strex sell option."""
    parameter = Parameter(
        strex_merchant_sell_option=strex_sell_option,
    )

    assert parameter.strex_merchant_sell_option == strex_sell_option
    assert type(parameter.strex_merchant_sell_option) is str
    assert parameter.strex_merchant_sell_option != ""
    assert parameter.strex_merchant_sell_option is not None


@pytest.mark.parametrize(
    "strex_confirm_channel",
    [
        "sms",
        "ussd",
    ],
)
def test_parameter_strex_confirm_channel_should_pass(strex_confirm_channel):
    """Test the parameter strex confirm channel."""
    parameter = Parameter(
        strex_confirm_channel=strex_confirm_channel,
    )

    assert parameter.strex_confirm_channel == strex_confirm_channel
    assert type(parameter.strex_confirm_channel) is str
    assert parameter.strex_confirm_channel != ""
    assert parameter.strex_confirm_channel is not None


def test_parameter_strex_confirm_channel_otp_should_pass():
    """Test the parameter strex confirm channel."""
    with pytest.raises(_exceptions.InvalidStrexConfirmChannel):
        parameter = Parameter(
            strex_confirm_channel="otp",
        )


@pytest.mark.xfail(reason="missing mandatory parameter")
def test_parameter_strex_confirm_channel_otp_should_fail():
    """Test the parameter strex confirm channel."""
    parameter = Parameter(
        strex_confirm_channel="otp",  # type: ignore
    )


def test_parameter_list_should_pass():
    """Test the parameter list."""
    parameter = Parameter(
        strex_authorization_token="some_token",
        strex_verification_timeout="10",
    )

    assert parameter.list() == [
        {"key": "strex_verification_timeout", "value": "10"},
        {"key": "strex_authorization_token", "value": "some_token"},
    ]


def test_parameter_str_should_pass():
    """Test the parameter str."""
    parameter = Parameter(
        strex_authorization_token="some_token",
        strex_verification_timeout="10",
    )

    assert (
        parameter.__str__()
        == """[
    {
        "key": "strex_verification_timeout",
        "value": "10"
    },
    {
        "key": "strex_authorization_token",
        "value": "some_token"
    }
]"""
    )


@pytest.mark.xfail(raises=AssertionError)
def test_safe_remove_non_gsm_characters_deprecated_should_pass():
    """Test the safe remove non gsm characters deprecated."""
    message = (
        "safe_remove_non_gsm_characters is deprecated "
        "and will be removed in the next version."
    )

    message_settings = MessageSettings(
        # safe_remove_non_gsm_characters=True,
    )

    assert message_settings.safe_remove_non_gsm_characters is None

    message_settings.safe_remove_non_gsm_characters = True

    assert message == message_settings.__str__()
    assert message_settings.safe_remove_non_gsm_characters is not None

    assert message_settings.safe_remove_non_gsm_characters_deprecated is True
    assert message_settings.safe_remove_non_gsm_characters is True
