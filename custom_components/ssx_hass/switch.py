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

from .ssx_utils import exec_cmd_ret_out, exec_cmd_ret_code

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
    add_entities([N2ScreenSwitch(),MiniLightSwitch()])


def lock_sessions(lock_sessions: bool = True):
    lock = "" if lock_sessions else "un"
    # 锁定会话，解锁会话
    os.system(f"ssh root@node102 'echo loginctl {lock}lock-sessions > /root/exec_cmd.sh'")


def kill_time_background():
    exec_cmd_ret_code("ssh root@node102 kill -9 `ssh root@node102 ps -ef | grep gluqlo | awk '{print $2}'`")
    exec_cmd_ret_code("ssh root@node102 kill -9 `ssh root@node102 ps -ef | grep gluqlo | awk '{print $2}'`")
    exec_cmd_ret_code("ssh root@node102 kill -9 `ssh root@node102 ps -ef | grep gluqlo | awk '{print $2}'`")

class N2ScreenSwitch(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init N2ScreenSwitch start!')
        self._is_on: bool = exec_cmd_ret_out("ssh root@node102 'ps -ef | grep gluqlo'").find("/home/ssx/apps/gluqlo/gluqlo") > 0
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

    def update(self) -> None:
        _LOGGER.info('update N2ScreenSwitch start! %s', self._is_on)
        # /home/ssx/apps/gluqlo/gluqlo过滤有用！
        self._is_on = exec_cmd_ret_out("ssh root@node102 'ps -ef | grep gluqlo'").find("/home/ssx/apps/gluqlo/gluqlo") > 0

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
        time.sleep(3)
        # 显示屏保
        if not self._is_on:
            # root@node102:~# cat lock_background.sh
            # #!/bin/bash
            # export DISPLAY=:0.0
            # /home/ssx/apps/gluqlo/gluqlo -f -s 1.4
            # os.system("ssh root@node102 '~/lock_background.sh'")
            os.system(f"ssh root@node102 'echo /home/ssx/apps/gluqlo/gluqlo -f -s 1.4 > /root/exec_cmd.sh'")

    # 提前设置锁屏超时时间：永不
    def turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.info(f'turn_off.self={kwargs}')
        # 结束屏保
        kill_time_background()
        # 锁定会话
        time.sleep(6)
        lock_sessions()

class MiniLightSwitch(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init MiniLightSwitch start!')
        self._is_on: bool = True
        self._attr_device_info = "MiniLightSwitch_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "MiniLightSwitch_attr_unique_id"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug(f'extra_state_attributes Run')
        attributes = {
            'friendly_name': f'小小灯'
        }
        return attributes

    def update(self) -> None:
        _LOGGER.info('update MiniLightSwitch start! %s', self._is_on)
        # /home/ssx/apps/gluqlo/gluqlo过滤有用！


    @property
    def is_on(self):
        """If the switch is currently on or off."""
        _LOGGER.info('is_on.self------------')
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.info(f'turn_on.self={kwargs}')

        result = exec_cmd_ret_out("echo -e open_mini_light_GHJY_6_2_902 | nc 192.168.0.104 81", 10)
        _LOGGER.info("exec ret %s", result)
        self._is_on = str(result) == "open mini_light fenish"

    # 提前设置锁屏超时时间：永不
    def turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.info(f'turn_off.self={kwargs}')

        result = exec_cmd_ret_out("echo -e close_mini_light_GHJY_6_2_902 | nc 192.168.0.104 81", 10)
        _LOGGER.info("exec ret %s", result)
        if str(result) == "close mini_light fenish":
            self._is_on = False