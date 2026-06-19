"""Platform for notify integration."""
from __future__ import annotations

import datetime
import json

from homeassistant.components.notify import NotifyEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
import logging
import random
from ssx_utils import sendPostJson

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=10)


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
    add_entities([DeskScreenST7789()])


class DeskScreenST7789(NotifyEntity):
    _attr_has_entity_name = True
    BASE_URL = 'http://192.168.0.111:5557'

    def __init__(self):
        _LOGGER.info('init DeskScreenST7789 start!')
        self._attr_device_info = "ssx_DeskScreenST7789_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_DeskScreenST7789_attr_unique_id"

    # example
    # @param message  '{"message":"hello world","emoji":"2728"}'
    # @param title  'message_type'
    def send_message(self, message: str, title: str | None = None) -> None:
        """Send a message."""
        _LOGGER.info(f"send message, title: {title}, message: {message}")
        if title == 'message_type':
            msg = json.loads(message)
            resp = sendPostJson(self.BASE_URL, {
                "message": msg["message"],
                "emoji": msg["emoji"]
            })
            _LOGGER.info(f"resp: {resp}")

        elif title == 'image_type':
            img_path = message
