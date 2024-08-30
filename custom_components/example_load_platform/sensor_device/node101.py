"""Platform for sensor integration."""
from __future__ import annotations


from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import TEMP_CELSIUS

import logging

from custom_components.example_load_platform import ssx_utils

_LOGGER = logging.getLogger(__name__)
DellR410Info = ssx_utils.DellR410Info()
Node12CpuMem = None


class DellR410TemperatureSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "DellR410TemperatureSensorDevice"  # For automatic device registration
        self._attr_unique_id = "DellR410TemperatureSensorUnique"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'DellR410温度'

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
        global DellR410Info
        DellR410Info = ssx_utils.getDellR410Info()
        self._attr_native_value = DellR410Info.temperature


class DellR410SpeedSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "DellR410SpeedSensorDevice"  # For automatic device registration
        self._attr_unique_id = "DellR410SpeedSensorDeviceUnique"
        self._attr_device_class = SensorDeviceClass.SPEED

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'DellR410风扇转速'

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


class DellR410CpuSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "DellR410CpuSensorDevice"  # For automatic device registration
        self._attr_unique_id = "DellR410CpuSensorDeviceUnique"
        self._attr_device_class = SensorDeviceClass.HUMIDITY

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'DellR410处理器使用率'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        _LOGGER.debug('native_value DellR410CpuSensor !')
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        _LOGGER.debug('native_unit_of_measurement DellR410CpuSensor !')
        # FAN MOD 1A RPM   | 9960 RPM          | ok
        return "%"

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('update DellR410CpuSensor !')
        info: ssx_utils.DellR410Node12CpuMemInfo = ssx_utils.getNode12CpuMemInfo()
        _LOGGER.info(f'DellR410Node12CpuMemInfo:{info.cpuDesc}\n{info.memDesc}')
        self._attr_native_value = info.cpu



