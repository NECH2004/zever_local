from datetime import datetime
from enum import IntEnum
import logging

import httpx

_LOGGER = logging.getLogger(__name__)

# definition of values in string array (positions) as far as known
# see also: https://github.com/solmoller/eversolar-monitor/issues/22

# 0, 1 - unknown
# 2 - Registry ID - also MAC address
# 3 - Registry Key
# 4 - Hardware Version
# 5 - Software version
# 6 - Time and Date
# 7 - Communication status with ZeverCloud
# 8 - unknown
# 9 - SN.
# 10 - Pac(W)
# 11 - E_Today(KWh) - attention! Has a bug.
# 12 - Status
# 13 - unknown

# Attention:
# - if you split the byte array time and date will be two array entries.
# - E_Today(KWh) has a bug.


class ArrayPosition(IntEnum):
    """Defines the value position in the data array."""
    unknown0 = 0
    unknown1 = 1
    registry_id = 2
    registry_key = 3
    hardware_version = 4
    software_version = 5
    date_and_time = 6
    communication_status = 7
    unknown8 = 8
    serial_number = 9
    pac_watt = 10
    energy_today_KWh = 11
    status = 12
    unknown13 = 13


class ZeversolarError(Exception):
    """General problem.
    Possible causes:
        - The data stream is not as expected.
          This can sometimes be seen if the inverter tries to reconnect.
    """


class ZeversolarTimeout(ZeversolarError):
    """The inverter cannot be reached.
    Possible causes:
        - inverter is off (darkness)
        - wrong IP address
    """


class InverterData():
    def __init__(self, data_array: list[str]) -> None:
        self._unknown0 = data_array[ArrayPosition.unknown0]
        self._unknown1 = data_array[ArrayPosition.unknown1]
        registry_id = data_array[ArrayPosition.registry_id]
        self._registry_id = registry_id
        self._registry_key = data_array[ArrayPosition.registry_key]
        self._hardware_version = data_array[ArrayPosition.hardware_version]
        self._software_version = data_array[ArrayPosition.software_version]
        date_and_time = data_array[ArrayPosition.date_and_time]
        self._communication_status = data_array[ArrayPosition.communication_status]
        self._unknown8 = data_array[ArrayPosition.unknown0]
        self._serial_number = data_array[ArrayPosition.serial_number]
        self._pac_watt : int = int(data_array[ArrayPosition.pac_watt])
        val = data_array[ArrayPosition.energy_today_KWh]
        self._energy_today_KWh : float = float(self._patch(val))
        self._status = data_array[ArrayPosition.status]
        self._unknown13 = data_array[ArrayPosition.unknown13]
        self._mac_address = f"{registry_id[0:2]}-{registry_id[2:4]}-{registry_id[4:6]}-{registry_id[6:8]}-{registry_id[8:10]}-{registry_id[10:12]}"
        self._datetime = datetime.strptime(date_and_time, '%H:%M %d/%m/%Y')

    @property
    def unknown0(self) -> str:
        return self._unknown0

    @property
    def unknown1(self) -> str:
        return self._unknown1

    @property
    def registry_id(self) -> str:
        return self._registry_id

    @property
    def registry_key(self) -> str:
        return self._registry_key

    @property
    def hardware_version(self) -> str:
        return self._hardware_version

    @property
    def software_version(self) -> str:
        return self._software_version

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def communication_status(self) -> str:
        return self._communication_status

    @property
    def unknown8(self) -> str:
        return self._unknown8

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @property
    def pac_watt(self) -> int:
        return self._pac_watt

    @property
    def energy_today_KWh(self) -> float:
        return self._energy_today_KWh

    @property
    def status(self) -> str:
        return self._status

    @property
    def unknown13(self) -> str:
        return self._unknown13

    @property
    def mac_address(self) -> str:
        return self._mac_address

    def _patch(self, val: str) -> str:
        """Fix the missing 0 if only one decimal is given."""
        if (
            val[-2] == "."
        ):
            return val[0:-1] + "0" + val[-1:]
        return val


class Inverter():
    def __init__(self, ip_address: str, timeout: int = 5) -> None:
        self._ip_address : str = ip_address
        self._timeout : int = timeout
        self._mac_address : str = None
        self._serial_number : str = None

        self._local_data_url : str = f"http://{ip_address}/home.cgi"   # ?sid=0
        self._local_power_url : str = f"http://{ip_address}/inv_ctrl.cgi"   # ?sid=0

    @property
    def mac_address(self):
        return self._mac_address

    @property
    def serial_number(self):
        return self._serial_number

    async def async_connect(self) -> None:
        """Reads inverter related information from the url."""
        try:
            async with httpx.AsyncClient() as client:
                data = await client.get(self._local_data_url, timeout=self._timeout)

#                data_array2 = data.content.split()
                result_string = data.content.decode(encoding="utf-8")
                data_array = result_string.split('\n')

                registry_id = data_array[ArrayPosition.registry_id]
                serial_number = data_array[ArrayPosition.serial_number]
                mac_address = f"{registry_id[0:2]}-{registry_id[2:4]}-{registry_id[4:6]}-{registry_id[6:8]}-{registry_id[8:10]}-{registry_id[10:12]}"

        except httpx.TimeoutException as ex:
            raise ZeversolarTimeout(f"Connection to Zeversolar inverter '{self._ip_address}' timed out.") from ex
        except Exception as ex:
            raise ZeversolarError(f"Generic error while connecting to Zeversolar inverter '{self._ip_address}'.") from ex

        self._mac_address = mac_address
        self._serial_number = serial_number

    async def async_get_data(self) -> InverterData:
        """Reads the actual data from the inverter."""
        try:
            async with httpx.AsyncClient() as client:
                data = await client.get(self._local_data_url, timeout=self._timeout)
                result_string = data.content.decode(encoding="utf-8")
                data_array = result_string.split('\n')
        except httpx.TimeoutException as ex:
            raise ZeversolarTimeout(f"Connection to Zeversolar inverter '{self._ip_address}' timed out.") from ex
        except Exception as ex:
            raise ZeversolarError(f"Generic error while connecting to Zeversolar inverter '{self._ip_address}'.") from ex

        return InverterData(data_array)

    async def power_on(self) -> bool:
        """Power inverter on."""
        return await self._change_power_state(0)

    async def power_off(self) -> bool:
        """Power inverter off."""
        return await self._change_power_state(1)

    async def _change_power_state(self, mode : int) -> bool:
        """Power inverter on or off."""
        try:
            async with httpx.AsyncClient() as client:
                my_response = await client.post(self._local_power_url, data={'sn': self._serial_number, 'mode': mode}, timeout=self._timeout)
                return my_response.status_code == 200

        except httpx.TimeoutException as ex:
            raise ZeversolarTimeout(f"Connection to Zeversolar inverter '{self._ip_address}' timed out.") from ex
        except Exception as ex:
            raise ZeversolarError(f"Generic error while connecting to Zeversolar inverter '{self._ip_address}'.") from ex
