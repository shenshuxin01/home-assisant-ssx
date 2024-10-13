"""Platform for sensor integration."""
from __future__ import annotations

import datetime
import os
import time

from homeassistant.components.cover import CoverEntity, CoverEntityFeature, CoverDeviceClass, ATTR_POSITION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

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
    add_entities([Window1()])


#卧室窗户
#       command_on: echo -e 'run_2_9' | nc 192.168.0.106 80
#       command_off: echo -e 'run_4_9' | nc 192.168.0.106 80
# return 1-9
def cal_position(p) -> str:
    position = int(p)
    position = min(max(position, 0), 99)
    if position < 10:
        return "0" + str(position)
    return str(position)


# True开窗
# 转多少秒
def exec_cmd(direction_flag: bool, seconds) -> str:
    direction = 2 if direction_flag else 4
    result = os.popen(f"echo -e 'run_{direction}_{seconds}' | nc 192.168.0.106 80").readlines()[0]
    logging.info("exec window %s", result)
    return result


class Window1(CoverEntity):
    """Representation of a Window1."""
    _attr_has_entity_name = True

    def __init__(self) -> None:
        """Initialize the sensor."""
        super().__init__()
        self._attr_device_info = "ssx_device_info_Window1"  # For automatic device registration
        self._attr_unique_id = "ssx_unique_id_Window1"
        self._attr_current_cover_position: int | None = None
        self._attr_is_closed = True
        self._attr_is_closing = False
        self._attr_is_opening = False
        # my properties
        self.running_p = 0  # 0表示没有任务 正数表示打开中 负数表示关闭中

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return '窗户'

    @property
    def device_classes(self) -> str:
        """Return the name of the sensor."""
        return CoverDeviceClass.WINDOW

    @property
    def supported_features(self):
        return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.SET_POSITION | CoverEntityFeature.STOP

    def update(self) -> None:
        logging.info("update called")
        if (self._attr_current_cover_position is None) or self._attr_current_cover_position == 0:
            self._attr_is_closed = True
            self._attr_is_closing = False
            self._attr_is_opening = False
        elif self._attr_current_cover_position == 100:
            self._attr_is_closed = False
            self._attr_is_closing = False
            self._attr_is_opening = False
        else:
            self._attr_is_closed = False
        if self.running_p == 0:
            self._attr_is_closing = False
            self._attr_is_opening = False
        if self.running_p > 0:
            self._attr_is_closing = False
            self._attr_is_opening = True
        if self.running_p < 0:
            self._attr_is_closing = True
            self._attr_is_opening = False

    def check_window(self) -> None:
        if self._attr_current_cover_position is None:
            self.running_p = -9
            exec_cmd(False, 9)
            self._attr_current_cover_position = 0
            self.running_p = 0

    def open_cover(self, **kwargs):
        """Open the cover."""
        self.check_window()
        self.running_p = 9
        exec_cmd(True, 9)
        self._attr_current_cover_position = 100
        self.running_p = 0

    def close_cover(self, **kwargs):
        """Close cover."""
        self.check_window()
        self.running_p = -9
        exec_cmd(False, 9)
        self._attr_current_cover_position = 0
        self.running_p = 0

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        self.check_window()
        logging.info("Setting position to %s", kwargs.get(ATTR_POSITION))
        position: str = cal_position(kwargs.get(ATTR_POSITION))
        if position == "00":
            self.close_cover()
            return
        if position == "99":
            self.open_cover()
            return
        if self.running_p != 0:
            for i in range(1, 10):
                time.sleep(1)
                if self.running_p == 0:
                    self.set_cover_position(position=kwargs.get(ATTR_POSITION))
                    break
            return
        targe_first = int(position[0])
        current_first = int(cal_position(self._attr_current_cover_position)[0])
        self.running_p = targe_first - current_first
        for i in range(1, 10):
            if self.running_p == 0:
                self._attr_current_cover_position = kwargs.get(ATTR_POSITION)
                return
            if self.running_p > 0:
                # 开窗1秒
                self._attr_current_cover_position += 10
                exec_cmd(True, 1)
                self.running_p -= 1
            elif self.running_p < 0:
                # 关窗1秒
                self._attr_current_cover_position -= 10
                exec_cmd(False, 1)
                self.running_p += 1
        self.running_p = 0
        self._attr_current_cover_position = kwargs.get(ATTR_POSITION)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self.running_p = 0
