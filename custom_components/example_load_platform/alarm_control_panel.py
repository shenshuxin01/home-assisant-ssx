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
    _attr_state = 'arming'

    @property
    def supported_features(self):
        return AlarmControlPanelEntityFeature.ARM_HOME \
               | AlarmControlPanelEntityFeature.ARM_AWAY \
               | AlarmControlPanelEntityFeature.ARM_NIGHT \
               | AlarmControlPanelEntityFeature.TRIGGER \
               | AlarmControlPanelEntityFeature.ARM_CUSTOM_BYPASS \
               | AlarmControlPanelEntityFeature.ARM_VACATION

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init Node12AlarmControlPanel start!')
        self._attr_device_info = "ssx_Node12AlarmControlPanel_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_Node12AlarmControlPanel_attr_unique_id"

    def alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        _LOGGER.info(f'alarm_disarm Run')

    def alarm_arm_home(self, code=None) -> None:
        """Send arm home command."""
        _LOGGER.info(f'alarm_arm_home Run')

    def alarm_arm_away(self, code=None) -> None:
        """Send arm away command."""
        _LOGGER.info(f'alarm_arm_away Run')

    def alarm_arm_night(self, code=None) -> None:
        """Send arm night command."""
        _LOGGER.info(f'alarm_arm_night Run')

    def alarm_arm_vacation(self, code=None) -> None:
        """Send arm vacation command."""
        _LOGGER.info(f'alarm_arm_vacation Run')

    def alarm_trigger(self, code=None) -> None:
        """Send alarm trigger command."""
        _LOGGER.info(f'alarm_trigger Run')

    def alarm_arm_custom_bypass(self, code=None) -> None:
        """Send arm custom bypass command."""
        _LOGGER.info(f'alarm_arm_custom_bypass Run')

    def update(self) -> None:
        _LOGGER.info(f'update.method run!')
        self._attr_changed_by = f'ssx_{str(random.randint(1, 10))}'
        r = random.randint(1, 10)
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
        if r == 1:
            self._attr_state = 'disarmed'
        elif r == 2:
            self._attr_state = 'armed_home'
        elif r == 3:
            self._attr_state = 'armed_away'
        elif r == 4:
            self._attr_state = 'armed_night'
        elif r == 5:
            self._attr_state = 'armed_vacation'
        elif r == 6:
            self._attr_state = 'armed_custom_bypass'
        elif r == 7:
            self._attr_state = 'pending'
        elif r == 8:
            self._attr_state = 'arming'
        elif r == 9:
            self._attr_state = 'disarming'
        elif r == 10:
            self._attr_state = 'triggered'
