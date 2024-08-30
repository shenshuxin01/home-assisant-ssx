"""Platform for sensor integration."""
from __future__ import annotations

import datetime


from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

from .sensor_device.node101 import DellR410TemperatureSensor, DellR410SpeedSensor, DellR410CpuSensor
from .sensor_device.node109 import Node109GPUSensor,Node109CPUSensor
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=60)


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
    add_entities([DellR410TemperatureSensor(), DellR410SpeedSensor(), DellR410CpuSensor(), Node109GPUSensor(), Node109CPUSensor()])



