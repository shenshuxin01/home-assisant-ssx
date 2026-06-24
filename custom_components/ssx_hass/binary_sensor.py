"""Platform for sensor integration."""
from __future__ import annotations

import datetime
import time

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

from . import DOMAIN
from .ssx_utils import exec_cmd_ret_out, sendTcpData

_LOGGER = logging.getLogger(__name__)



# 冰箱门开关传感器，因为冰箱有时候关不紧
SCAN_INTERVAL = datetime.timedelta(seconds=5)


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
    add_entities([IceBinarySensor(),DeskPersonExistsBinarySensor()])


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
        #为什么是三遍呢？ 这个传感器不准
        result = exec_cmd_ret_out("echo -e eeSx671Status | nc 192.168.0.104 81 && echo -e eeSx671Status | nc 192.168.0.104 81 && echo -e eeSx671Status | nc 192.168.0.104 81", 10)
        # switch0switch0switch0
        _LOGGER.info("exec ret %s", result)
        if str(result) == "switch1switch1switch1":
            self._attr_is_on = True
        elif str(result) == "switch0switch0switch0":
            self._attr_is_on = False


class DeskPersonExistsBinarySensor(BinarySensorEntity):
    """Representation of a sensor."""
    # 深圳市海凌科电子有限公司 https://r0.hlktech.com/download/HLK-LD2410C-24G/1/HLK%20LD2410C生命存在感应模组说明书V1.09.pdf
    # HLK - LD2410C
    # 人体存在感应模组
    HOST = '192.168.0.107'
    PORT = 9997
    last_update_time = time.perf_counter()*1000

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_is_on = None
        self._attr_device_info = "DeskPersonExistsBinarySensorDevice"  # For automatic device registration
        self._attr_unique_id = "DeskPersonExistsBinarySensorDeviceUnique"
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return '电脑桌人体存在传感器'

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update DeskPersonExistsBinarySensorDevice !')
        resp = sendTcpData(self.HOST, self.PORT, {"cmd": "hasPerson"})

        _LOGGER.info("exec ret %s", resp)
        if resp["success"]:
            if resp["exists"]:
                self._attr_is_on = True
            else:
                self._attr_is_on = False
        else:
            self._attr_is_on = None
