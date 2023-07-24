"""Platform for text integration."""
from __future__ import annotations

import time
from datetime import timedelta

from homeassistant.components.text import TextEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
import logging
import random

_LOGGER = logging.getLogger(__name__)


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
    add_entities([DemoText(hass)], update_before_add=True)


class DemoText(TextEntity):
    _attr_has_entity_name = True
    # The value of the text.
    _attr_native_value = 'DemoText'

    SCAN_INTERVAL = timedelta(seconds=5)

    def __init__(self,hass):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=10)
        )
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init DemoText start!')
        self._attr_device_info = "ssx_DemoText_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_DemoText_attr_unique_id"

    def update(self) -> None:
        self._attr_native_value = f'myssxText_{random.randint(1, 4500)}'
        _LOGGER.info(f'update.method run!')

    def set_value(self, value: str) -> None:
        """Set the text value."""
        _LOGGER.info(f'set_value.method run!:{value}')
        self._attr_native_value = value

