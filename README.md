# Zeversolar local

[![PyPi](https://img.shields.io/pypi/v/zeversolar_local.svg)](https://pypi.python.org/pypi/zeversolar_local/)
[![Python Versions](https://img.shields.io/pypi/pyversions/zeversolar_local.svg)](https://github.com/NECH2004/zeversolar_local/)
[![Build Status](https://github.com/NECH2004/zeversolar_local/actions/workflows/publish.yaml/badge.svg)](https://github.com/NECH2004/zeversolar_local/actions/workflows/publish.yaml)
![License](https://img.shields.io/github/license/NECH2004/zeversolar_local.svg)

Library for connecting to a Zeversolar inverter over local network. Retrieves the inverter data.

Only tested on a Zeversolar 2000.
## Usage

1. Install this package `pip install zeversolar_local`
2. Connect to your inverter using its IP address (192.168.5.101, e.g.) and fetch the data

```python
from src.zeversolar_local.inverter import (
    Inverter,
    InverterData,
    ZeversolarError,
    ZeversolarTimeout,
)

async def async_get_data():
    ip_address = "192.168.5.101"
    my_inverter = Inverter(url)

    my_inverter_data = await my_inverter.async_get_data()
    energy_today_KWh = my_inverter_data.energy_today_KWh

```
