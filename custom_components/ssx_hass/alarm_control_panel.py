"""Platform for alarm_control_panel integration."""
from __future__ import annotations

import datetime
import json
import time

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, CodeFormat, \
    AlarmControlPanelEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN, ssx_utils
import logging
import random

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=120)

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
    add_entities([Node12AlarmControlPanel()])
    # hass.states.set("alarm_control_panel.example_load_platform_Node12AlarmControlPanelDeviceUnique",
    #                 'armed_home')


# https://developers.home-assistant.io/docs/core/entity/alarm-control-panel
class Node12AlarmControlPanel(AlarmControlPanelEntity):
    _attr_has_entity_name = True
    # changed_by	string	None	Describes what the last change was triggered by.
    _attr_changed_by = 'ssx001'
    # code_format	string	None	Regex for code format or None if no code is required.
    _attr_code_format = CodeFormat.TEXT

    # States
    # Value	Description
    # disarmed	The alarm is disarmed (off).
    # armed_home	The alarm is armed in home mode.
    # armed_away	The alarm is armed in away mode.
    # armed_night	The alarm is armed in night mode.
    # armed_vacation	The alarm is armed in vacation mode.
    # armed_custom_bypass 	The alarm is armed in bypass mode.
    # pending	The alarm is pending (towards triggered).
    # arming	The alarm is arming.
    # disarming	The alarm is disarming.
    # triggered	The alarm is triggered.
    _attr_state = 'armed_home'

    @property
    def supported_features(self):
        return AlarmControlPanelEntityFeature.ARM_HOME \
               | AlarmControlPanelEntityFeature.ARM_AWAY \
               | AlarmControlPanelEntityFeature.ARM_NIGHT

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init Node12AlarmControlPanel start!')
        self._attr_device_info = "Node12AlarmControlPanelDevice"  # For automatic device registration
        self._attr_unique_id = "Node12AlarmControlPanelDeviceUnique"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return '巩华家园监控面板'

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug(f'extra_state_attributes Run')
        attributes = {
            'ssx_diy': f'myssx_{random.randint(1, 10)}'
        }
        return attributes

    def alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        _LOGGER.info(f'alarm_disarm Run,codeInfo:{code}')
        self._attr_state = 'disarming'
        time.sleep(1)
        self._attr_state = 'disarmed'
        ssx_utils.play_text_homepod('alarm_disarm')

    def alarm_arm_home(self, code=None) -> None:
        """Send arm home command."""
        _LOGGER.info(f'alarm_arm_home Run,codeInfo:{code}')
        self._attr_state = 'armed_home'
        ssx_utils.play_text_homepod('alarm_arm_home')

    def alarm_arm_away(self, code=None) -> None:
        """Send arm away command."""
        _LOGGER.info(f'alarm_arm_away Run,codeInfo:{code}')
        self._attr_state = 'armed_away'
        ssx_utils.play_text_homepod('alarm_arm_away')

    def alarm_arm_night(self, code=None) -> None:
        """Send arm night command."""
        _LOGGER.info(f'alarm_arm_night Run,codeInfo:{code}')
        self._attr_state = 'armed_night'
        ssx_utils.play_text_homepod('alarm_arm_night')

    def alarm_trigger(self, code=None) -> None:
        """Send alarm trigger command."""
        _LOGGER.info(f'alarm_trigger Run,codeInfo:{code}')
        self._attr_state = 'triggered'

    def update(self) -> None:
        _LOGGER.info(f'update.method run!,state:{self._attr_state}')
        # disarmed	The alarm is disarmed (off).
        # armed_home	The alarm is armed in home mode.
        # armed_away	The alarm is armed in away mode.
        # armed_night	The alarm is armed in night mode.
        # armed_vacation	The alarm is armed in vacation mode.
        # armed_custom_bypass 	The alarm is armed in bypass mode.
        # pending	The alarm is pending (towards triggered).
        # arming	The alarm is arming.
        # disarming	The alarm is disarming.
        # triggered	The alarm is triggered.
        # if 陌生人来访：
        #     self._attr_state = 'arming'
        # if 陌生人进门啦：
        #     self.alarm_trigger(None)

        if 'disarmed'.__eq__(self._attr_state):
            return

        # info: ssx_utils.DellR410Node12CpuMemInfo = ssx_utils.getNode12CpuMemInfo()
        # _LOGGER.info(f'DellR410Node12CpuMemInfo:{info.cpuDesc}\n{info.memDesc}')
        # if float(info.cpu) > 500:
        #     _LOGGER.error(f'CPU异常:{info.cpuDesc}')
        #     self._attr_state = 'pending'
        #     self.alarm_trigger(None)
        # elif float(info.mem) > 80:
        #     _LOGGER.error(f'MEM异常:{info.memDesc}')
        #     self._attr_state = 'pending'
        #     self.alarm_trigger(None)

