# Zeversolar local

[![PyPi][pypi-shield]][pypi-address]
[![Python Versions][pypi-version-shield]][github-address]
[![Build Status](https://github.com/NECH2004/zever_local/actions/workflows/publish.yaml/badge.svg)](https://github.com/NECH2004/zever_local/actions/workflows/publish.yaml)

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield_y]][commits]
[![GitHub Activity][commits-shield_m]][commits]
[![GitHub Activity][commits-shield_w]][commits]


[![Validate][validate-shield]][validation]


Library for connecting to a Zeversolar inverter over local network. Retrieves the inverter data.

Only tested on a Zeversolar 2000.
## Usage

1. Install this package `pip install zever_local`
2. Connect to your inverter using its IP address (192.168.5.101, e.g.) and fetch the data

```python
from zever_local.inverter import (
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
[releases-shield]: https://img.shields.io/github/v/release/NECH2004/zever_local?style=for-the-badge
[releases]: https://github.com/NECH2004/zever_local/releases

[commits-shield_y]: https://img.shields.io/github/commit-activity/y/NECH2004/zever_local?style=for-the-badge
[commits-shield_m]: https://img.shields.io/github/commit-activity/m/NECH2004/zever_local?style=for-the-badge
[commits-shield_w]: https://img.shields.io/github/commit-activity/w/NECH2004/zever_local?style=for-the-badge
[commits]: https://github.com/NECH2004/zever_local/commits/dev

[validate-shield]: https://github.com/NECH2004/zever_local/actions/workflows/validate.yml/badge.svg?branch=dev
[validation]: https://github.com/NECH2004/zever_local/actions/workflows/validate.yml

[license-shield]:https://img.shields.io/github/license/NECH2004/zever_local?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Christian%20Neumeier%20%40NECH2004?style=for-the-badge

[pypi-shield]: https://img.shields.io/pypi/v/zever_local.svg?style=for-the-badge
[pypi-address]: https://pypi.python.org/pypi/zever_local/
[pypi-version-shield]: https://img.shields.io/pypi/pyversions/zever_local.svg?style=for-the-badge
[github-address]: https://github.com/NECH2004/zever_local/
