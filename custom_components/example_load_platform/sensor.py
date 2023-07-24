"""Platform for sensor integration."""
from __future__ import annotations

import datetime
import random

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN, ssx_utils
import logging

_LOGGER = logging.getLogger(__name__)
DellR410Info = {"fanSpeed": "-1", "temperature": -1}
Next_Update = datetime.datetime.now()
Node12CpuMem = None

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
    add_entities([DellR410TemperatureSensor(), DellR410SpeedSensor(), Node12CpuMemSensor()])


class DellR410TemperatureSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "ssx_device_info_DellR410TemperatureSensor"  # For automatic device registration
        self._attr_unique_id = "ssx_unique_id_DellR410TemperatureSensor"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Dell_R410_Temperature_Sensor'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        _LOGGER.debug('native_value DellR410TemperatureSensor !')
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        _LOGGER.debug('native_unit_of_measurement DellR410TemperatureSensor !')
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update DellR410TemperatureSensor !')
        global DellR410Info, Next_Update
        if datetime.datetime.now() < Next_Update:
            _LOGGER.debug('下次执行时间未到，不执行')
            return
        else:
            _LOGGER.debug('下次执行时间到啦，执行')
            Next_Update = datetime.datetime.now() + datetime.timedelta(minutes=1)
        DellR410Info = ssx_utils.getDellR410Info()
        self._attr_native_value = DellR410Info.temperature


class DellR410SpeedSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "ssx_device_info_DellR410SpeedSensor"  # For automatic device registration
        self._attr_unique_id = "ssx_unique_id_DellR410SpeedSensor"
        self._attr_device_class = SensorDeviceClass.SPEED

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Dell_R410_Speed_Sensor'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        _LOGGER.debug('native_value DellR410SpeedSensor !')
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        _LOGGER.debug('native_unit_of_measurement DellR410SpeedSensor !')
        # FAN MOD 1A RPM   | 9960 RPM          | ok
        return "RPM"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update DellR410SpeedSensor !')
        global DellR410Info
        self._attr_native_value = DellR410Info.speed


class Node12CpuMemSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "ssx_device_info_Node12CpuMemSensor"  # For automatic device registration
        self._attr_unique_id = "ssx_unique_id_Node12CpuMemSensor"
        # self._attr_device_class = SensorDeviceClass.SPEED

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Node12CpuMemSensor_Sensor'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        _LOGGER.debug('native_value Node12CpuMemSensor !')
        return self._attr_native_value

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update Node12CpuMemSensor !')
        global Node12CpuMem
        # Node12CpuMem = ssx_utils.getNode12CpuMemInfo()
        # self._attr_native_value = Node12CpuMem
        self._attr_native_value = f'myssxNode12CpuMemSensor_{random.randint(1, 4500)}'




