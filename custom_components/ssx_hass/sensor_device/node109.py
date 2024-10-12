"""Platform for sensor integration."""
from __future__ import annotations

import requests
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import TEMP_CELSIUS

import logging

from custom_components.ssx_hass import ssx_utils

_LOGGER = logging.getLogger(__name__)


class Node109GPUSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "Node109GPUSensorDevice"  # For automatic device registration
        self._attr_unique_id = "Node109GPUSensorUnique"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Node109GPU温度'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        resp = requests.get(
            'http://192.168.0.109:5000/getNode109GPUSensor')
        # {'temperature': '30', 'speed': 8448.0}
        if resp.status_code != 200:
            raise IOError('请求node109 CPU Temperature 接口失败！！')
        respJson = resp.json()  # {"fanSpeed":"7920","temperature":32}
        self._attr_native_value = respJson['gpu']


class Node109CPUSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_native_value = None
        self._attr_device_info = "Node109CPUSensorDevice"  # For automatic device registration
        self._attr_unique_id = "Node109CPUSensorUnique"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Node109CPU温度'

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        resp = requests.get(
            'http://192.168.0.109:5000/getNode109CPUSensor')
        # {'temperature': '30', 'speed': 8448.0}
        if resp.status_code != 200:
            raise IOError('请求node109 CPU Temperature 接口失败！！')
        respJson = resp.json()  # {"fanSpeed":"7920","temperature":32}
        self._attr_native_value = respJson['cpu']
