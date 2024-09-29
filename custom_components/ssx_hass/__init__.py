"""Example Load Platform integration."""
from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = 'ssx_hass'


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {
        'temperature': 23,
        'ssxVar1': 'hello world'
    }

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('lock', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('camera', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform(Platform.ALARM_CONTROL_PANEL, DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('text', DOMAIN, {}, config)

    return True
