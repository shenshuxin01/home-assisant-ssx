"""Platform for alarm_control_panel integration."""
from __future__ import annotations

import time

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, CodeFormat, \
    AlarmControlPanelEntityFeature
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
    add_entities([Node12AlarmControlPanel()])
    hass.states.set("alarm_control_panel.example_load_platform_ssx_node12alarmcontrolpanel_attr_unique_id", 'hello ssx extra')


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
               | AlarmControlPanelEntityFeature.ARM_NIGHT \
               | AlarmControlPanelEntityFeature.TRIGGER \
               | AlarmControlPanelEntityFeature.ARM_CUSTOM_BYPASS \
               | AlarmControlPanelEntityFeature.ARM_VACATION

    @property
    def code_format(self):
        return CodeFormat('v11','nmes12')

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init Node12AlarmControlPanel start!')
        self._attr_device_info = "ssx_Node12AlarmControlPanel_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_Node12AlarmControlPanel_attr_unique_id"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.info(f'extra_state_attributes Run')
        # return f'myssxNode12AlarmControlPanel_extra_state_attributes_{random.randint(1, 4500)}' 默认30s刷新一次
        attributes = {
            'ssx_diy': f'myssxNode12AlarmControlPanel_extra_state_attributes_{random.randint(1, 4500)}',
            'friendly_name': f'报警了吗:{random.randint(1, 4500)}',
        }
        return attributes

    def alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        _LOGGER.info(f'alarm_disarm Run,codeInfo:{code}')
        self._attr_state = 'disarming'
        time.sleep(1)
        self._attr_state = 'disarmed'

    def alarm_arm_home(self, code=None) -> None:
        """Send arm home command."""
        _LOGGER.info(f'alarm_arm_home Run,codeInfo:{code}')
        self._attr_state = 'armed_home'

    def alarm_arm_away(self, code=None) -> None:
        """Send arm away command."""
        _LOGGER.info(f'alarm_arm_away Run,codeInfo:{code}')
        self._attr_state = 'armed_away'

    def alarm_arm_night(self, code=None) -> None:
        """Send arm night command."""
        _LOGGER.info(f'alarm_arm_night Run,codeInfo:{code}')
        self._attr_state = 'armed_night'

    def alarm_arm_vacation(self, code=None) -> None:
        """Send arm vacation command."""
        _LOGGER.info(f'alarm_arm_vacation Run,codeInfo:{code}')
        self._attr_state = 'armed_vacation'

    def alarm_trigger(self, code=None) -> None:
        """Send alarm trigger command."""
        _LOGGER.info(f'alarm_trigger Run,codeInfo:{code}')
        self._attr_state = 'pending'
        time.sleep(1000)
        self._attr_state = 'triggered'

    def alarm_arm_custom_bypass(self, code=None) -> None:
        """Send arm custom bypass command."""
        _LOGGER.info(f'alarm_arm_custom_bypass Run,codeInfo:{code}')
        self._attr_state = 'armed_custom_bypass'

    def update(self) -> None:
        self._attr_changed_by = f'ssx_{str(random.randint(1, 10))}'
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
        _LOGGER.info(f'update.method run!,state:{self._attr_state}')