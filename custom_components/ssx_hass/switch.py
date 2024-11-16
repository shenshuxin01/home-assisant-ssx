"""Platform for sensor integration."""
from __future__ import annotations

import os
import time

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
import logging
import datetime

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=120)


def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the switch platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities([N2ScreenSwitch()])


def lock_sessions(lock_sessions: bool = True):
    lock = "" if lock_sessions else "un"
    # 锁定会话，解锁会话
    os.system(f"sudo loginctl {lock}lock-sessions")


class N2ScreenSwitch(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init N2ScreenSwitch start!')
        self._is_on = True
        self._attr_device_info = "N2ScreenSwitch_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "N2ScreenSwitch_attr_unique_id"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug(f'extra_state_attributes Run')
        attributes = {
            'friendly_name': f'屏幕时间'
        }
        return attributes

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        _LOGGER.info('is_on.self------------')
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.info(f'turn_on.self={kwargs}')

        # 解锁会话
        lock_sessions(False)
        time.sleep(1)
        # 显示屏保
        os.system("kill -9 `ps -ef | grep gluqlo | awk '{print $2}'`")
        os.system("nohup /home/ssx/apps/gluqlo/gluqlo -f -s 1.4 >/dev/null 2>&1 &")
        self._is_on = True

    # 提前设置锁屏超时时间：永不
    def turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.info(f'turn_off.self={kwargs}')

        # 锁定会话
        lock_sessions()
        time.sleep(1)
        # 结束屏保
        os.system("kill -9 `ps -ef | grep gluqlo | awk '{print $2}'`")
        self._is_on = False

