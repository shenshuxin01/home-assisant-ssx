"""Platform for text integration."""
from __future__ import annotations

import datetime
import json

from homeassistant.components.text import TextEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN, ssx_utils
import logging
import random

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=120)

def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities([DellR410CpuText()])


class DellR410CpuText(TextEntity):
    _attr_has_entity_name = True
    # The value of the text.
    _attr_native_value = ''

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init DellR410CpuText start!')
        self._attr_device_info = "ssx_DellR410CpuText_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_DellR410CpuText_attr_unique_id"

    def update(self) -> None:
        _LOGGER.info(f'update.method run!')
        info: ssx_utils.DellR410Node12CpuMemInfo = ssx_utils.getNode12CpuMemInfo()
        self._attr_native_value = f'cpu:{info.cpu}\n' \
                                  f'cpuDesc:{info.cpuDesc}\n' \
                                  f'mem:{info.mem}\n' \
                                  f'memDesc:{info.memDesc}'

    def set_value(self, value: str) -> None:
        """Set the text value."""
        _LOGGER.info(f'set_value.method run!:{value}')
        self._attr_native_value = value

