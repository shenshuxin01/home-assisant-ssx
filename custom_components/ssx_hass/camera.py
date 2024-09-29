"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components import ffmpeg

from homeassistant.components.camera import (
    SUPPORT_ON_OFF,
    SUPPORT_STREAM,
    Camera, StreamType
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging


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
    add_entities([EzvizCamera()])


def getStreamSource() ->str:
    # streamURL = f"rtsp://admin:AGXXZI@192.168.0.105:554/h264/ch1/main/av_stream"
    streamURL = f"rtsp://admin:AGXXZI@192.168.0.105:554/h264/ch2/sub/av_stream"
    return streamURL


class EzvizCamera(Camera):
    """Representation of a sensor."""
    _attr_has_entity_name = True

    def __init__(self) -> None:
        """Initialize the sensor."""
        super().__init__()
        self._attr_device_info = "ssx_device_info_EzvizCamera"  # For automatic device registration
        self._attr_unique_id = "ssx_unique_id_EzvizCamera"
        self._attr_is_recording = True
        self._attr_is_streaming = True
        self._attr_is_on = True
        self._attr_frontend_stream_type = StreamType.HLS

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Ezviz_Camera'

    @property
    def supported_features(self):
        return SUPPORT_STREAM | SUPPORT_ON_OFF

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        with open('/config/ezviz.webp', "rb") as file:
            return file.read()

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return getStreamSource()

    def turn_on(self) -> None:
        """Turn on camera."""

    def turn_off(self) -> None:
        """Turn off camera."""
