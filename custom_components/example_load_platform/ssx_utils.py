import logging

import requests

_LOGGER = logging.getLogger(__name__)

class DellR410Info:
    temperature = None
    speed = None

    def __init__(self):
        self.temperature: float
        self.speed: float


class DellR410Node12CpuMemInfo:
    cpu: float = None
    cpuDesc: str = None
    mem: float = None
    memDesc: str = None


def getDellR410Info() -> DellR410Info:
    resp = requests.get(
        'http://192.168.0.101:5000/autoSetDellFanOnceTempAndSpeed')
    # {'temperature': '30', 'speed': 8448.0}
    if resp.status_code != 200:
        raise IOError('请求dell风扇转速Python接口失败！！')
    respJson = resp.json()  #{"fanSpeed":"7920","temperature":32}
    d = DellR410Info()
    d.temperature = respJson['temperature']
    d.speed = respJson['fanSpeed']
    return d


def getNode12CpuMemInfo() -> DellR410Node12CpuMemInfo:
    resp = requests.get(
        'http://192.168.0.101:5000/get_node12_cpu_mem_df_info')
    # {
    #     "cpu": "16.0",
    #     "cpuDesc": " root 16.0 0.1 /usr/local/bin/ffmpeg -v info -t 77572 -i rtsp://admin:AGXXZI@192.168.0.105:554/h264/ch1/sub/av_stream -force_key_frames expr:gte(t,n_forced*1) -hls_time 60 -threads 1 -hls_list_size 0 -hls_segment_filename /ssxtmp/index_1690223228_%20d.ts /ssxtmp/index_1690223228.m3u8 \n",
    #     "mem": "3.4",
    #     "memDesc": " root 0.8 3.4 java -DuserLogbackLevel=error -Dloader.path=/home/app/apps/k8s/for_docker_volume/jenkins/jars/eureka-server -jar /myappjar/app.jar --spring.profiles.active=prod \n"
    # }
    if resp.status_code != 200:
        raise IOError('请求node12内存处理器信息Python接口失败！！')
    respJson = resp.json()  #{"fanSpeed":"7920","temperature":32}
    d2 = DellR410Node12CpuMemInfo()
    d2.cpu = respJson['cpu']
    d2.cpuDesc = respJson['cpuDesc']
    d2.mem = respJson['mem']
    d2.memDesc = respJson['memDesc']
    return d2


def play_text_xiaoai(text: str) -> None:
    resp = requests.post(
        "http://node109:8123/api/services/tts/xiaomo_say",
        data='{"entity_id": "media_player.xiao_ai_yin_xiang_3783","message": "' + text + '","cache": true}',
        headers= {'Content-Type': 'application/json;charset=UTF-8','Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzZjUyOWUwMjNmOWQ0M2UxOTVkYTIyZWY2MmNkZmQ0MyIsImlhdCI6MTcyNDc0MTcyOSwiZXhwIjoyMDQwMTAxNzI5fQ.5KFgbSC71-Cn8lJkejmhfiDdOTZQ2PInM6k8aJYK_p8'}
    )
    if resp.status_code != 200:
        _LOGGER.error('error'+resp.reason)
        return
    respJson = resp.json()
    _LOGGER.debug(respJson)


if __name__ == '__main__':
     play_text_xiaoai('nihao')