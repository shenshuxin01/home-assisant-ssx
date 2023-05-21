"""Platform for sensor integration."""
from __future__ import annotations

import time

from homeassistant.components.lock import LockEntity
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
    add_entities([ExampleLock()])


class ExampleLock(LockEntity):
    _attr_has_entity_name = True
    # changed_by	string	None	Describes what the last change was triggered by.
    _attr_changed_by = 'ssx001'
    # code_format	string	None	Regex for code format or None if no code is required.
    # _attr_code_format = 'ssx001'
    # is_locked	bool	None	Indication of whether the lock is currently locked. Used to determine state.
    _attr_is_locked = False
    # is_locking	bool	None	Indication of whether the lock is currently locking. Used to determine state.
    _attr_is_locking = True
    # is_unlocking	bool	None	Indication of whether the lock is currently unlocking. Used to determine state.
    _attr_is_unlocking = True
    # is_jammed	bool	None	Indication of whether the lock is currently jammed. Used to determine state.
    _attr_is_jammed = False

    def update(self) -> None:
        self._attr_is_jammed = random.randint(1, 4500) == 2
        _LOGGER.info(f'update.method run!self._attr_is_jammed={self._attr_is_jammed}')

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init ExampleLock start!')
        self._attr_device_info = "ssx_ExampleLock_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_ExampleLock_attr_unique_id"

    def lock(self, **kwargs):
        """Lock all or specified locks. A code to lock the lock with may optionally be specified."""
        _LOGGER.info(f'lock.kwargs={kwargs}')
        self._attr_is_locking = True
        time.sleep(3)
        self._attr_is_locking = False
        self._attr_is_locked = True
        self._attr_is_unlocking = False

    def unlock(self, **kwargs):
        """Unlock all or specified locks. A code to unlock the lock with may optionally be specified."""
        _LOGGER.info(f'unlock.kwargs={kwargs}')
        self._attr_is_unlocking = True
        time.sleep(3)
        self._attr_is_unlocking = False
        self._attr_is_locked = False
        self._attr_is_locking = False

    # async def async_lock(self, **kwargs):
    #     """Lock all or specified locks. A code to lock the lock with may optionally be specified."""
    #     _LOGGER.info(f'async_lock.kwargs={kwargs}')
    #     self._attr_is_locking = True
    #     time.sleep(10)
    #     self._attr_is_locking = False
    #     self._attr_is_locked = True
    #     self._attr_is_unlocking = False
