"""Platform for sensor integration."""
from __future__ import annotations

import datetime

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

from . import DOMAIN
from .ssx_utils import exec_cmd_ret_out

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=3)

# 冰箱门开关传感器，因为冰箱有时候关不紧


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
    add_entities([IceBinarySensor()])


class IceBinarySensor(BinarySensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_is_on = None
        self._attr_device_info = "IceBinarySensorDevice"  # For automatic device registration
        self._attr_unique_id = "IceBinarySensorDeviceUnique"
        self._attr_device_class = BinarySensorDeviceClass.DOOR

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return '冰箱门传感器'

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update IceBinarySensorDevice !')
        result = exec_cmd_ret_out("echo -e eeSx671Status | nc 192.168.0.104 81", 10)
        _LOGGER.info("exec ret %s", result)
        if str(result) == "switch1":
            self._attr_is_on = True
        elif str(result) == "switch0":
            self._attr_is_on = False
        else:
            _LOGGER.error("IceBinarySensorDevice status check fail! not ask resp on 192.168.0.104")
            self._attr_is_on = None


