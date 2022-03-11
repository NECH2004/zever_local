from unittest.mock import patch
from datetime import datetime

import httpx
import pytest

from src.zeversolar_local.inverter import (
    Inverter,
    InverterData,
    ZeversolarError,
    ZeversolarTimeout,
)

_registry_id = "EAB241277A36"
_registry_key = "ZYXTBGERTXJLTSVS"
_hardware_version = "M11"
_software_version = "18625-797R+17829-719R"
_time = "16:22"
_date = "20/02/2022"
_serial_number = "ZS150045138C0104"
_content = f"1\n1\n{_registry_id}\n{_registry_key}\n{_hardware_version}\n{_software_version}\n{_time} {_date}\n1\n1\n{_serial_number}\n1234\n8.9\nOK\nError"
_content2 = f"1\n1\n{_registry_id}\n{_registry_key}\n{_hardware_version}\n{_software_version}\n{_time} {_date}\n1\n1\n{_serial_number}\n1234\n1.23\nOK\nError"

_byte_content = _content.encode()


async def test_async_connect():
    """Fetch the inverter info."""
    url = "test"
    my_inverter = Inverter(url)

    mock_response = httpx.Response(
        200, request=httpx.Request("Get", "https://test.t"), content=_byte_content
    )

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
        mock_device_info.return_value = mock_response

        await my_inverter.async_connect()

    mac_address = my_inverter.mac_address
    serial_number = my_inverter.serial_number

    assert mac_address == "EA-B2-41-27-7A-36"
    assert serial_number == _serial_number


async def test_async_get_data():
    """Fetch inverter data."""
    url = "test"
    my_inverter = Inverter(url)

    mock_response = httpx.Response(
        200, request=httpx.Request("Get", f"https://{url}"), content=_byte_content
    )

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
        mock_device_info.return_value = mock_response

        my_inverter_data = await my_inverter.async_get_data()

    energy_today_KWh = my_inverter_data.energy_today_KWh

    assert energy_today_KWh == 8.09

async def test_async_get_data_ZeversolarError():
    """Fetch inverter data throws an error."""
    url = "test"
    with pytest.raises(ZeversolarError):
        my_inverter = Inverter(url)
        await my_inverter.async_get_data()

async def test_async_get_data_ZeversolarTimeout():
    """Fetch inverter data timouts."""
    url = "test"
    with pytest.raises(ZeversolarTimeout):
        with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
            mock_device_info.side_effect = httpx.TimeoutException("Timeout")

            my_inverter = Inverter(url)
            await my_inverter.async_get_data()

async def test_async_connect_ZeversolarError():
    """Connect to inverter data throws an error."""
    url = "test"
    with pytest.raises(ZeversolarError):
        my_inverter = Inverter(url)
        await my_inverter.async_connect()

async def test_async_connect_ZeversolarTimeout():
    """Connect to inverter data timouts."""
    url = "test"
    with pytest.raises(ZeversolarTimeout):
        with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
            mock_device_info.side_effect = httpx.TimeoutException("Timeout")

            my_inverter = Inverter(url)
            await my_inverter.async_connect()

def test_InverterData():
    """Test the inverter data class."""
    my_inverter_data = InverterData(_content2.split('\n'))

    energy_today_KWh = my_inverter_data.energy_today_KWh
    unknown0 = my_inverter_data.unknown0
    unknown1 = my_inverter_data.unknown1
    registry_id = my_inverter_data.registry_id
    registry_key = my_inverter_data.registry_key
    hardware_version = my_inverter_data.hardware_version
    software_version = my_inverter_data.software_version
    my_datetime = my_inverter_data.datetime
    communication_status = my_inverter_data.communication_status
    unknown8 = my_inverter_data.unknown8
    serial_number = my_inverter_data.serial_number
    pac_watt = my_inverter_data.pac_watt
    energy_today_KWh = my_inverter_data.energy_today_KWh
    status = my_inverter_data.status
    unknown13 = my_inverter_data.unknown13
    mac_address = my_inverter_data.mac_address

    assert unknown0 == '1'
    assert unknown1 == '1'
    assert registry_id == _registry_id
    assert registry_key == _registry_key
    assert hardware_version == _hardware_version
    assert software_version == _software_version
    assert datetime(2022, 2, 20, 16, 22) == my_datetime
    assert communication_status == '1'
    assert unknown8 == '1'
    assert serial_number == _serial_number
    assert pac_watt == 1234
    assert energy_today_KWh == 1.23
    assert status == 'OK'
    assert unknown13 == "Error"
    assert mac_address == "EA-B2-41-27-7A-36"


def test_InverterData_bugfix():
    """Test the inverter data class fixing the energy bug."""
    my_inverter_data = InverterData(_content.split('\n'))

    energy_today_KWh = my_inverter_data.energy_today_KWh

    assert energy_today_KWh == 8.09


async def test_Inverter_power_on():
    """Power on inverter."""
    url = "test"
    my_inverter = Inverter(url)

    mock_response = httpx.Response(
        200, request=httpx.Request("Get", f"https://{url}"), content=_byte_content
    )

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
        mock_device_info.return_value = mock_response

        my_inverter = Inverter(url)
        await my_inverter.async_connect()

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.post") as mock_device_info:
        mock_device_info.return_value = mock_response

        my_result = await my_inverter.power_on()

    assert my_result


async def test_Inverter_power_off():
    """Power on inverter."""
    url = "test"
    my_inverter = Inverter(url)

    mock_response = httpx.Response(
        200, request=httpx.Request("Get", f"https://{url}"), content=_byte_content
    )

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.get") as mock_device_info:
        mock_device_info.return_value = mock_response

        my_inverter = Inverter(url)
        await my_inverter.async_connect()

    with patch("src.zeversolar_local.inverter.httpx.AsyncClient.post") as mock_device_info:
        mock_device_info.return_value = mock_response

        my_result = await my_inverter.power_off()

    assert my_result


async def test_Inverter_power_on_ZeversolarError():
    """Power off inverter."""
    url = "test"
    my_inverter = Inverter(url)

    with pytest.raises(ZeversolarError):

        my_inverter = Inverter(url)
        await my_inverter.power_on()


async def test_Inverter_power_on_ZeversolarTimeout():
    """Power off inverter has a timeout."""
    url = "test"
    my_inverter = Inverter(url)

    with pytest.raises(ZeversolarTimeout):
        with patch("src.zeversolar_local.inverter.httpx.AsyncClient.post") as mock_device_info:
            mock_device_info.side_effect = httpx.TimeoutException("Timeout")

            my_inverter = Inverter(url)
            await my_inverter.power_on()
