"""Platform for sensor integration."""
from __future__ import annotations

import time

from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEnqueue, MediaType
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# from . import DOMAIN
import logging
import random
import subprocess

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
    add_entities([Node102MediaPlayer()])


class Node102MediaPlayer(MediaPlayerEntity):

    def __init__(self):
        #         _LOGGER.info(f'turn_on.kwargs={kwargs}')
        _LOGGER.info('init Node102MediaPlayer start!')
        self._attr_device_info = "ssx_Node102MediaPlayer_attr_device_info"  # For automatic device registration
        self._attr_unique_id = "ssx_Node102MediaPlayer_attr_unique_id"

    def update(self) -> None:
        self._attr_is_jammed = random.randint(1, 4500) == 2
        _LOGGER.info(f'update.method run!self._attr_is_jammed={self._attr_is_jammed}')


    def play_media(
        self,
        media_type: str,
        media_id: str,
        enqueue: MediaPlayerEnqueue | None = None,
        announce: bool | None = None, **kwargs
    ) -> None:
        """Play a piece of media."""

        result = subprocess.check_output(
            ["yt-dlp", "-g",
             "--add-header", "Origin:https://www.bilibili.com",
             "--add-header", "Cookie: "+kwargs.get('cookie'),
             "--referer","https://www.bilibili.com/",url],
            text=True
        )

        video_url, audio_url = result.strip().splitlines()[:2]

        # print(video_url)
        #
        # print(audio_url)

        mpv_cmd = f"export DISPLAY=:0 && \
        mpv --start=00:15:11 \
            '{video_url}' \
            --referrer='https://www.bilibili.com/' \
            --user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15' \
            --http-header-fields='Origin: https://www.bilibili.com' --fullscreen  \
            --audio-file='{audio_url}'"
        print(mpv_cmd)

        result = subprocess.check_output(
            ["ssh", "ssx@node102",
             "echo", f'"{mpv_cmd}"',
             ">", "/home/ssx/media_player_mpv.sh"],
            text=True
        )

        # result = subprocess.check_output(
        #     ["ssh", "ssx@node102",
        #      "sh", "/home/ssx/media_player_mpv.sh"],
        #     text=True
        # )
        print(result)



if __name__ == '__main__':
    vip_cookie = "b_lsid=1F7BDB1B_19EE6024E86; buvid4=DE8F6B6D-7D7E-0E85-D59E-911C5CEA179C59060-026061319-tzF4rXUqOJMi5TgdRcna5A%3D%3D; CURRENT_FNVAL=16; theme-tip-show=SHOWED; ogv_device_support_dolby=1; ogv_device_support_hdr=1; CURRENT_QUALITY=112; browser_resolution=1852-895; home_feed_column=5; bp_t_offset_266617553=1216055737151651840; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODIxOTkwOTgsImlhdCI6MTc4MTkzOTgzOCwicGx0IjotMX0.WuSMelEFuv306ojs00arL8ytQ8UrPV_ZpVW1m5d2EBg; bili_ticket_expires=1782199038; theme-avatar-tip-show=SHOWED; buvid_fp=832b90dce0443ab8537c903d9fa30e6d; _uuid=410A4A8F6-F8A3-9C106-7F84-10C2EB57FDA6C58936infoc; LIVE_BUVID=AUTO2517801386827184; rpdid=|(J~kku|YlYR0J'u~~~ukku|R; sid=5003ph29; DedeUserID=266617553; DedeUserID__ckMd5=8de60720b44b1452; SESSDATA=57bc2052%2C1792674092%2C09a61%2A42CjDqmfuzl-LZ9-G7QJ0rI8wP5CSz1XCwapVE0vyAZHBplHDeKJrwNRswqvV5k618ePcSVk1SS0hkSThUdnhTeEJOaHBaMGNPWlNKd0tHeldTTTFJdmk5eklMRnJEZDF0Q043amxVbGktNV92NFhabFNiNFJLQmFTTVJ5MDBQZEdySlRtT2dRaFNBIIEC; bili_jct=6a69d1d967ef8887e8bd4947478082cf; b_nut=1777122060; buvid3=9A47080F-E7EB-C29F-B4EB-C6B23F66DD6060192infoc"

    url = "https://www.bilibili.com/video/BV1RHjU6gEyj/?t=9&spm_id_from=333.1007.tianma.10-4-38.click&vd_source=5e62320d0e3f6c0251d17c49ce88b79d"

    Node102MediaPlayer().play_media(MediaType.VIDEO,url,cookie=vip_cookie)