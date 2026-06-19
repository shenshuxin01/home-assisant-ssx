import json
import logging

from homeassistant.components.notify import BaseNotificationService

from .ssx_utils import sendPostJson

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config, discovery_info=None):
    _LOGGER.info("Create SSX notify service")
    _LOGGER.info("config=%s", config)
    return SsxCustNotify()


# ssx_cust_notify
"""
action: notify.ssx_cust_notify
data:
  message: "{\"message\":\"hello world\",\"emoji\":\"1f44b\"}"
  title: message_type
"""
class SsxCustNotify(BaseNotificationService):
    BASE_URL = "http://192.168.0.111:5557/show_message"

    def send_message(self, message="", **kwargs):
        title = kwargs.get("title")

        _LOGGER.info(
            "send message title=%s message=%s",
            title,
            message,
        )

        try:
            if title == "message_type":
                msg = json.loads(message)

                resp = sendPostJson(
                    self.BASE_URL,
                    {
                        "message": msg["message"],
                        "emoji": msg["emoji"],
                    },
                )

                _LOGGER.info("resp=%s", resp)

        except Exception:
            _LOGGER.error("send notify failed")
